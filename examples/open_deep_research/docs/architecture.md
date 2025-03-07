# Open Deep Research Architecture Documentation

## Overview
Open Deep Research is a sophisticated document processing and analysis system that converts various file formats into markdown for AI processing. The system employs multiple converters and integrates with multimodal LLM capabilities for enhanced content understanding.

## Core Components

### MarkdownConverter
The central component that orchestrates the conversion of different file types to markdown format. Key features:
- Supports multiple file formats including DOCX, PDF, images, and more
- Implements a priority-based converter registration system
- Handles both local files and URLs
- Integrates with multimodal LLM for enhanced content processing

### Document Converters
Specialized converters for different file types:

1. **ImageConverter**
   - Processes image files (.jpg, .jpeg, .png)
   - Extracts metadata using exiftool
   - Generates image descriptions using multimodal LLM
   - Captures key metadata fields including:
     - ImageSize
     - Title
     - Caption
     - Description
     - Keywords
     - Artist
     - Author
     - DateTimeOriginal
     - CreateDate
     - GPSPosition

2. **DocxConverter**
   - Converts DOCX files to markdown
   - Preserves document structure and formatting
   - Maintains tables and heading styles
   - Uses mammoth library for HTML conversion

3. **Additional Converters**
   - PlainTextConverter
   - HtmlConverter
   - WikipediaConverter
   - YouTubeConverter
   - XlsxConverter
   - PptxConverter
   - WavConverter
   - Mp3Converter
   - ZipConverter
   - PdfConverter

## File Processing Flow

1. **Input Processing**
   - Accepts local files, URLs, or request responses
   - Determines file type through extensions and content analysis
   - Handles temporary file creation for streaming content

2. **Conversion Process**
   - Identifies appropriate converter based on file type
   - Applies converter-specific processing
   - Generates normalized markdown output
   - Handles errors and exceptions gracefully

3. **MLM Integration**
   - Supports multimodal LLM processing
   - Enables advanced content analysis
   - Provides rich descriptions for media content

## Error Handling
- Comprehensive error tracking and reporting
- Graceful fallback mechanisms
- Detailed error traces for debugging
- Support for multiple conversion attempts with different extensions

## Future Considerations
- Extensible architecture for new file types
- Modular design for easy updates
- Scalable processing capabilities
- Enhanced multimodal support

## Security Considerations
- Safe handling of temporary files
- Proper cleanup of resources
- Secure URL processing
- User-agent management for web requests

This documentation provides a comprehensive overview of the Open Deep Research system's architecture and components, serving as a reference for future development and maintenance.