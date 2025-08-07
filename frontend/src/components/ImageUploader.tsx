'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import { Upload, Image as ImageIcon } from 'lucide-react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Props {
  onResult: (result: any) => void
  onLoading: (loading: boolean) => void
}

export default function ImageUploader({ onResult, onLoading }: Props) {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string>('')

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    setFileName(file.name)
    
    // Show image preview
    const reader = new FileReader()
    reader.onload = () => setUploadedImage(reader.result as string)
    reader.readAsDataURL(file)

    // Upload and analyze
    onLoading(true)
    onResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      })

      onResult(response.data)
    } catch (error: any) {
      console.error('Upload error:', error)
      onResult({
        success: false,
        error: error.response?.data?.detail || 'Failed to analyze image'
      })
    } finally {
      onLoading(false)
    }
  }, [onResult, onLoading])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.webp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  })

  return (
    <div className="space-y-4">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-3">
          <Upload className="h-12 w-12 text-gray-400" />
          
          {isDragActive ? (
            <p className="text-blue-600 font-medium">Drop the image here...</p>
          ) : (
            <div>
              <p className="text-gray-600 font-medium">
                Drag & drop an image here, or click to select
              </p>
              <p className="text-sm text-gray-400 mt-1">
                Supports: JPG, PNG, WEBP (max 10MB)
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Image Preview */}
      {uploadedImage && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center space-x-3 mb-3">
            <ImageIcon className="h-5 w-5 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">
              {fileName}
            </span>
          </div>
          
          <img 
            src={uploadedImage} 
            alt="Uploaded preview"
            className="max-w-full max-h-64 mx-auto rounded-lg object-contain"
          />
        </div>
      )}
    </div>
  )
}
