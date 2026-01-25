import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, AlertCircle, CheckCircle, TrendingUp, Download } from 'lucide-react';
import { useResumeStore } from '../store/stores';
import { resumeAPI } from '../services/endpoints';
import Button from '../components/Button';
import Card from '../components/Card';
import toast from 'react-hot-toast';

const Resume = () => {
  const { resume, analysis, skillGaps, setResume, setAnalysis, setSkillGaps, clearResume } = useResumeStore((state) => ({
    resume: state.resume,
    analysis: state.analysis,
    skillGaps: state.skillGaps,
    setResume: state.setResume,
    setAnalysis: state.setAnalysis,
    setSkillGaps: state.setSkillGaps,
    clearResume: state.clearResume
  }));
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [localLoading, setLocalLoading] = useState(false);

  useEffect(() => {
    console.log('Analysis updated:', analysis);
    console.log('SkillGaps updated:', skillGaps);
  }, [analysis, skillGaps]);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  };

  const handleChange = (e) => {
    const files = e.target.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  };

  const processFile = async (uploadedFile) => {
    setError(null);
    const validTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];

    if (!validTypes.includes(uploadedFile.type)) {
      setError('Please upload a PDF, DOC, or DOCX file');
      toast.error('Invalid file type');
      return;
    }

    if (uploadedFile.size > 5 * 1024 * 1024) {
      setError('File size should be less than 5MB');
      toast.error('File too large');
      return;
    }

    setFile(uploadedFile);
    setResume({
      name: uploadedFile.name,
      size: uploadedFile.size,
      type: uploadedFile.type,
      uploadedAt: new Date().toISOString()
    });

    toast.success('Resume uploaded successfully!');
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a resume first');
      return;
    }

    setLocalLoading(true);
    try {
      // Upload resume and get extracted text
      const uploadResponse = await resumeAPI.uploadResume(file);
      console.log('Upload response:', uploadResponse);
      
      if (!uploadResponse.data || !uploadResponse.data.data) {
        throw new Error('Failed to extract resume text');
      }

      const extractedText = uploadResponse.data.data;

      // Analyze resume using the extracted text
      const analysisResponse = await resumeAPI.analyzResume(extractedText);
      console.log('Analysis response:', analysisResponse);
      
      if (analysisResponse.data?.data) {
        setAnalysis(analysisResponse.data.data);
        console.log('Analysis set:', analysisResponse.data.data);
      }

      // Get skill gaps
      const skillGapsResponse = await resumeAPI.getSkillGaps(extractedText, '');
      console.log('Skill gaps response:', skillGapsResponse);
      
      if (skillGapsResponse.data?.data) {
        setSkillGaps(skillGapsResponse.data.data);
        console.log('Skill gaps set:', skillGapsResponse.data.data);
      }

      toast.success('Resume analyzed successfully!');
    } catch (err) {
      const errorMessage = err.response?.data?.message || err.message || 'Failed to analyze resume';
      setError(errorMessage);
      toast.error(errorMessage);
      console.error('Resume analysis error:', err);
    } finally {
      setLocalLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <div className="pt-24 pb-12 px-4 sm:px-6 min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-4xl mx-auto"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">Resume Analyzer</h1>
          <p className="text-slate-400">Upload your resume to get AI-powered analysis and skill recommendations</p>
        </motion.div>

        {!resume ? (
          // Upload Section
          <motion.div
            variants={itemVariants}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`relative mb-8 p-12 border-2 border-dashed rounded-xl transition-all cursor-pointer ${
              dragActive
                ? 'border-slate-600 bg-slate-700/10'
                : 'border-slate-700 hover:border-slate-600'
            }`}
          >
            <input
              type="file"
              id="resume-upload"
              onChange={handleChange}
              accept=".pdf,.doc,.docx"
              className="hidden"
            />
            <label htmlFor="resume-upload" className="cursor-pointer">
              <div className="flex flex-col items-center gap-4">
                <motion.div
                  animate={{ y: dragActive ? -5 : 0 }}
                  className="p-4 bg-slate-700/20 rounded-lg"
                >
                  <Upload className="w-12 h-12 text-slate-400" />
                </motion.div>
                <div className="text-center">
                  <h2 className="text-xl font-semibold text-white mb-1">
                    {dragActive ? 'Drop your resume here' : 'Drag and drop your resume'}
                  </h2>
                  <p className="text-slate-400">or click to browse</p>
                  <p className="text-sm text-slate-500 mt-2">PDF, DOC, or DOCX • Max 5MB</p>
                </div>
              </div>
            </label>
          </motion.div>
        ) : (
          // File Info Section
          <motion.div variants={itemVariants} className="mb-8">
            <Card className="border-green-700/50">
              <div className="flex items-center gap-4 mb-4">
                <div className="p-3 bg-green-500/20 rounded-lg">
                  <FileText className="w-6 h-6 text-green-400" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-white">{resume.name}</h3>
                  <p className="text-sm text-slate-400">{(resume.size / 1024).toFixed(2)} KB</p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    clearResume();
                    setFile(null);
                    setAnalysis(null);
                    setSkillGaps(null);
                    setError(null);
                  }}
                >
                  Change
                </Button>
              </div>
              {!analysis && (
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  loading={localLoading}
                  onClick={handleAnalyze}
                  className="mt-4"
                >
                  Analyze Resume
                </Button>
              )}
            </Card>
          </motion.div>
        )}

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-3 p-4 bg-red-900/20 border border-red-700 rounded-lg mb-8 text-red-400"
          >
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p>{error}</p>
          </motion.div>
        )}

        {analysis && (
          <motion.div variants={containerVariants} className="space-y-6">
            {/* Analysis Results */}
            <motion.div variants={itemVariants}>
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <CheckCircle className="w-6 h-6 text-green-400" />
                Analysis Results
              </h2>
              <Card>
                <div className="space-y-6">
                  {/* Skills */}
                  <div>
                    <h3 className="font-semibold text-white mb-3">Skills Identified</h3>
                    <div className="flex flex-wrap gap-2">
                      {analysis.skills?.map((skill, idx) => (
                        <motion.span
                          key={idx}
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ delay: idx * 0.05 }}
                          className="px-3 py-1.5 bg-slate-600/30 text-slate-300 rounded-full text-sm border border-slate-500/50"
                        >
                          {skill}
                        </motion.span>
                      ))}
                    </div>
                  </div>

                  {/* Experience & Education */}
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-slate-400 text-sm mb-1">Experience</p>
                      <p className="text-white font-semibold">{analysis.experience}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-sm mb-1">Education</p>
                      <p className="text-white font-semibold">{analysis.education}</p>
                    </div>
                  </div>

                  {/* Job Role */}
                  <div>
                    <p className="text-slate-400 text-sm mb-1">Recommended Job Roles</p>
                    <p className="text-white font-semibold">{analysis.jobRole}</p>
                  </div>

                  {/* Projects */}
                  {analysis.projects && analysis.projects.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-white mb-3">Projects</h4>
                      <ul className="space-y-2">
                        {analysis.projects.map((project, idx) => (
                          <motion.li
                            key={idx}
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            transition={{ delay: idx * 0.1 }}
                            className="flex gap-3 text-slate-300"
                          >
                            <span className="text-slate-400 flex-shrink-0">•</span>
                            <span>{project}</span>
                          </motion.li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </Card>
            </motion.div>

            {/* Skill Gaps */}
            {skillGaps && (
              <motion.div variants={itemVariants}>
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <TrendingUp className="w-6 h-6 text-slate-400" />
                  Skill Gap Analysis
                </h2>

                <div className="space-y-4">
                  {/* Profile Summary */}
                  <Card>
                    <h3 className="font-semibold text-white mb-2">Profile Summary</h3>
                    <p className="text-slate-300">{skillGaps.profile_summary}</p>
                  </Card>

                  {/* Strengths */}
                  <Card className="bg-gradient-to-br from-green-900/20 to-emerald-900/20 border-green-700/30">
                    <h3 className="font-semibold text-green-300 mb-3">Strengths</h3>
                    <ul className="space-y-2">
                      {skillGaps.strengths?.map((strength, idx) => (
                        <motion.li
                          key={idx}
                          initial={{ x: -20, opacity: 0 }}
                          animate={{ x: 0, opacity: 1 }}
                          transition={{ delay: idx * 0.05 }}
                          className="flex gap-2 text-green-100"
                        >
                          <span className="text-green-400">✓</span>
                          <span>{strength}</span>
                        </motion.li>
                      ))}
                    </ul>
                  </Card>

                  {/* Weaknesses */}
                  <Card className="bg-gradient-to-br from-orange-900/20 to-red-900/20 border-orange-700/30">
                    <h3 className="font-semibold text-orange-300 mb-3">Areas for Improvement</h3>
                    <ul className="space-y-2">
                      {skillGaps.weaknesses?.map((weakness, idx) => (
                        <motion.li
                          key={idx}
                          initial={{ x: -20, opacity: 0 }}
                          animate={{ x: 0, opacity: 1 }}
                          transition={{ delay: idx * 0.05 }}
                          className="flex gap-2 text-orange-100"
                        >
                          <span className="text-orange-400">!</span>
                          <span>{weakness}</span>
                        </motion.li>
                      ))}
                    </ul>
                  </Card>

                  {/* Improvement Recommendations */}
                  <Card className="bg-gradient-to-br from-slate-800/20 to-slate-900/20 border-slate-700/30">
                    <h3 className="font-semibold text-slate-300 mb-3">Recommended Learning Path</h3>
                    <ol className="space-y-2">
                      {skillGaps.areas_of_improvement?.map((area, idx) => (
                        <motion.li
                          key={idx}
                          initial={{ x: -20, opacity: 0 }}
                          animate={{ x: 0, opacity: 1 }}
                          transition={{ delay: idx * 0.05 }}
                          className="flex gap-3 text-slate-100"
                        >
                          <span className="font-semibold text-slate-400 flex-shrink-0">{idx + 1}.</span>
                          <span>{area}</span>
                        </motion.li>
                      ))}
                    </ol>
                  </Card>
                </div>
              </motion.div>
            )}

            {/* Action Buttons */}
            <motion.div variants={itemVariants} className="flex gap-4 pt-6">
              <Button
                variant="secondary"
                size="lg"
                onClick={() => {
                  clearResume();
                  setFile(null);
                  setAnalysis(null);
                  setSkillGaps(null);
                  setError(null);
                }}
              >
                Analyze Another Resume
              </Button>
              <Button variant="outline" size="lg">
                <Download className="w-4 h-4" />
                Download Report
              </Button>
            </motion.div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default Resume;
