'use client'
import { useState, useRef } from 'react'
import styles from './page.module.css'

export default function Home() {
  const [image, setImage] = useState<string>('')
  const [caption, setCaption] = useState<string>('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Show image preview
    setImage(URL.createObjectURL(file))

    // Upload to backend
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    })
    const data = await response.json()
    setCaption(data.caption)
  }

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>SUPER AMAZING CAPTION MACHINE!</h1>
      <button 
        className={styles.uploadButton}
        onClick={() => fileInputRef.current?.click()}
      >
        CHOOSE FILE
      </button>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleUpload}
        className={styles.hiddenInput}
      />
      {image && <img src={image} alt="Uploaded" className={styles.image} />}
      {caption && <p className={styles.caption}>{caption}</p>}
    </main>
  )
} 