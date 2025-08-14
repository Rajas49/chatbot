"""
Document processing utilities for content retrieval and ranking
"""

import os
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from pathlib import Path

class DocumentProcessor:
    """Handles document loading, processing, and ranking"""
    
    def __init__(self, config):
        self.config = config
        self.embedder = SentenceTransformer(config['embedding_model'])
        self.min_similarity = config['min_similarity_threshold']
        self.max_docs = config['max_documents']
    
    def rank_documents(self, user_prompt, folders, top_k=None, min_similarity=None):
        """
        Rank documents based on similarity to user prompt
        
        Args:
            user_prompt: User's query
            folders: List of folder paths to search
            top_k: Maximum number of documents to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of tuples (similarity, filename, content)
        """
        if top_k is None:
            top_k = self.max_docs
        if min_similarity is None:
            min_similarity = self.min_similarity
            
        query_embedding = self.embedder.encode(user_prompt, convert_to_tensor=True)
        results = []
        
        for folder in folders:
            folder_results = self._process_folder(folder, query_embedding, min_similarity)
            results.extend(folder_results)
        
        # Sort by similarity and return top results
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:top_k]
    
    def _process_folder(self, folder_path, query_embedding, min_similarity):
        """Process all documents in a folder"""
        results = []
        
        if not os.path.exists(folder_path):
            st.warning(f"⚠️ Folder not found: {folder_path}")
            return results
        
        st.write(f"🔍 Searching in: {folder_path}")
        
        # Get all text files in folder
        folder = Path(folder_path)
        text_files = list(folder.glob("*.txt"))
        
        if not text_files:
            st.write(f"📄 No text files found in {folder_path}")
            return results
        
        processed_count = 0
        for file_path in text_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if not content:
                    continue
                
                # Create combined text for better matching
                filename = file_path.name
                combined_text = f"{filename} {content[:1000]}"  # Use first 1000 chars
                
                # Calculate similarity
                doc_embedding = self.embedder.encode(combined_text, convert_to_tensor=True)
                similarity = util.pytorch_cos_sim(query_embedding, doc_embedding).item()
                
                if similarity >= min_similarity:
                    results.append((similarity, filename, content))
                    st.write(f"✅ {filename}: {similarity:.3f}")
                    processed_count += 1
                else:
                    st.write(f"⚪ {filename}: {similarity:.3f} (below threshold)")
                    
            except Exception as e:
                st.warning(f"Error processing {file_path}: {str(e)}")
        
        st.write(f"📊 Processed {processed_count} relevant documents from {len(text_files)} files")
        return results
    
    def load_document_content(self, file_path):
        """Load content from a specific document"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            st.error(f"Error loading document {file_path}: {str(e)}")
            return None
    
    def get_document_summary(self, content, max_length=200):
        """Generate a summary of document content"""
        if not content:
            return "No content available"
        
        # Simple extractive summary - take first paragraph or sentences
        sentences = content.split('.')
        summary = ""
        
        for sentence in sentences:
            if len(summary + sentence) > max_length:
                break
            summary += sentence.strip() + ". "
        
        return summary.strip() or content[:max_length] + "..."
    
    def search_documents_by_keywords(self, keywords, folders):
        """Search documents using keyword matching"""
        results = []
        
        for folder_path in folders:
            if not os.path.exists(folder_path):
                continue
                
            folder = Path(folder_path)
            for file_path in folder.glob("*.txt"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                    
                    # Count keyword matches
                    matches = sum(1 for keyword in keywords if keyword.lower() in content)
                    
                    if matches > 0:
                        # Calculate simple relevance score
                        relevance = matches / len(keywords)
                        results.append((relevance, file_path.name, content, matches))
                        
                except Exception as e:
                    st.warning(f"Error searching {file_path}: {str(e)}")
        
        # Sort by relevance
        results.sort(reverse=True, key=lambda x: x[0])
        return results
    
    def get_folder_statistics(self, folder_path):
        """Get statistics about documents in a folder"""
        if not os.path.exists(folder_path):
            return None
        
        folder = Path(folder_path)
        text_files = list(folder.glob("*.txt"))
        
        if not text_files:
            return {"file_count": 0, "total_size": 0, "avg_size": 0}
        
        total_size = 0
        file_sizes = []
        
        for file_path in text_files:
            try:
                size = os.path.getsize(file_path)
                total_size += size
                file_sizes.append(size)
            except:
                continue
        
        return {
            "file_count": len(text_files),
            "total_size": total_size,
            "avg_size": total_size / len(text_files) if text_files else 0,
            "largest_file": max(file_sizes) if file_sizes else 0,
            "smallest_file": min(file_sizes) if file_sizes else 0
        }
    
    def validate_document_structure(self, folder_path):
        """Validate document structure and content quality"""
        issues = []
        
        if not os.path.exists(folder_path):
            issues.append(f"Folder does not exist: {folder_path}")
            return issues
        
        folder = Path(folder_path)
        text_files = list(folder.glob("*.txt"))
        
        if not text_files:
            issues.append(f"No text files found in {folder_path}")
            return issues
        
        for file_path in text_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common issues
                if len(content.strip()) < 50:
                    issues.append(f"File too short: {file_path.name}")
                
                if not any(char.isalpha() for char in content):
                    issues.append(f"No alphabetic content: {file_path.name}")
                
                # Check encoding issues
                try:
                    content.encode('utf-8')
                except UnicodeError:
                    issues.append(f"Encoding issue: {file_path.name}")
                    
            except Exception as e:
                issues.append(f"Cannot read file {file_path.name}: {str(e)}")
        
        return issues