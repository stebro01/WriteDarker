/**
 * Window Manager Service
 * Handles opening documents in new browser windows and communication between them
 */

class WindowManager {
  constructor() {
    this.openWindows = new Map() // documentId -> window reference
    this.windowCallbacks = new Map() // windowId -> callback functions
    this.setupMessageListener()
  }

  /**
   * Open a document in a new window
   * @param {Object} document - Document object
   * @param {Object} options - Window options
   * @returns {Window|null} - Reference to opened window
   */
  openDocumentWindow(document, options = {}) {
    const {
      width = 1200,
      height = 800,
      left = (screen.width - 1200) / 2,
      top = (screen.height - 800) / 2
    } = options

    // Close existing window for this document if it exists
    this.closeDocumentWindow(document.id)

    // Build window features string
    const features = [
      `width=${width}`,
      `height=${height}`,
      `left=${left}`,
      `top=${top}`,
      'scrollbars=yes',
      'resizable=yes',
      'status=no',
      'toolbar=no',
      'menubar=no',
      'location=no'
    ].join(',')

    // Create window URL with document data
    const windowUrl = this.createDocumentWindowUrl(document)
    
    // Open the window
    const newWindow = window.open(windowUrl, `document_${document.id}`, features)
    
    if (newWindow) {
      // Store window reference
      this.openWindows.set(document.id, newWindow)
      
      // Set up close listener
      const checkClosed = setInterval(() => {
        if (newWindow.closed) {
          clearInterval(checkClosed)
          this.openWindows.delete(document.id)
          this.notifyWindowClosed(document.id)
        }
      }, 1000)
      
      // Send initial data to window when it loads
      const sendInitialData = () => {
        try {
          // Convert reactive proxy to plain object for postMessage
          const plainDocument = JSON.parse(JSON.stringify(document))
          this.sendToWindow(newWindow, 'INIT_DOCUMENT', { document: plainDocument })
          console.log('Sent initial document data to window:', plainDocument.label)
        } catch (error) {
          console.error('Error sending initial data:', error)
        }
      }
      
      // Try multiple ways to ensure data is sent
      newWindow.addEventListener('load', sendInitialData)
      
      // Also try after a short delay in case load event doesn't fire
      setTimeout(() => {
        if (!newWindow.closed) {
          sendInitialData()
        }
      }, 1000)
    }

    return newWindow
  }

  /**
   * Open a media file in a new window
   * @param {Object} media - Media object
   * @param {Object} options - Window options
   * @returns {Window|null} - Reference to opened window
   */
  openMediaWindow(media, options = {}) {
    const {
      width = 1000,
      height = 700,
      left = (screen.width - 1000) / 2,
      top = (screen.height - 700) / 2
    } = options

    // Close existing window for this media if it exists
    this.closeMediaWindow(media.id)

    // Build window features string
    const features = [
      `width=${width}`,
      `height=${height}`,
      `left=${left}`,
      `top=${top}`,
      'scrollbars=yes',
      'resizable=yes',
      'status=no',
      'toolbar=no',
      'menubar=no',
      'location=no'
    ].join(',')

    // Create window URL with media data
    const windowUrl = this.createMediaWindowUrl(media)
    
    // Open the window
    const newWindow = window.open(windowUrl, `media_${media.id}`, features)
    
    if (newWindow) {
      // Store window reference using media ID with 'media_' prefix to avoid conflicts
      this.openWindows.set(`media_${media.id}`, newWindow)
      
      // Set up close listener
      const checkClosed = setInterval(() => {
        if (newWindow.closed) {
          clearInterval(checkClosed)
          this.openWindows.delete(`media_${media.id}`)
          this.notifyWindowClosed(`media_${media.id}`)
        }
      }, 1000)
      
      // Send initial data to window when it loads
      const sendInitialData = () => {
        try {
          // Convert reactive media to plain object for postMessage
          const plainMedia = JSON.parse(JSON.stringify(media))
          this.sendToWindow(newWindow, 'INIT_MEDIA', { media: plainMedia })
          console.log('Sent initial media data to window:', plainMedia.filename || plainMedia.label)
        } catch (error) {
          console.error('Error sending initial media data:', error)
        }
      }
      
      // Flag to prevent multiple sends
      let dataSent = false
      
      // Try multiple ways to ensure data is sent, but only once
      const sendOnce = () => {
        if (!dataSent && !newWindow.closed) {
          sendInitialData()
          dataSent = true
        }
      }
      
      newWindow.addEventListener('load', sendOnce)
      
      // Also try after a short delay in case load event doesn't fire
      setTimeout(sendOnce, 1000)
      
      console.log('Media opened in new window:', media.filename || media.label)
    }

    return newWindow
  }

  /**
   * Create URL for media window
   * @param {Object} media - Media object
   * @returns {string} - Window URL
   */
  createMediaWindowUrl(media) {
    // Create a standalone HTML page for media preview
    const baseUrl = window.location.origin
    return `${baseUrl}/media-window.html?id=${media.id}`
  }

  /**
   * Close a media window
   * @param {number} mediaId - Media ID
   */
  closeMediaWindow(mediaId) {
    const window = this.openWindows.get(`media_${mediaId}`)
    if (window && !window.closed) {
      window.close()
    }
    this.openWindows.delete(`media_${mediaId}`)
  }

  /**
   * Create URL for document window
   * @param {Object} document - Document object
   * @returns {string} - Window URL
   */
  createDocumentWindowUrl(document) {
    // Create a standalone HTML page for the document editor
    const baseUrl = window.location.origin
    return `${baseUrl}/document-window.html?id=${document.id}`
  }

  /**
   * Close a document window
   * @param {number} documentId - Document ID
   */
  closeDocumentWindow(documentId) {
    const window = this.openWindows.get(documentId)
    if (window && !window.closed) {
      window.close()
    }
    this.openWindows.delete(documentId)
  }

  /**
   * Send message to a specific window
   * @param {Window} targetWindow - Target window
   * @param {string} type - Message type
   * @param {Object} data - Message data
   */
  sendToWindow(targetWindow, type, data) {
    if (targetWindow && !targetWindow.closed) {
      targetWindow.postMessage({
        type,
        data,
        source: 'main_window'
      }, window.location.origin)
    }
  }

  /**
   * Send message to document window
   * @param {number} documentId - Document ID
   * @param {string} type - Message type
   * @param {Object} data - Message data
   */
  sendToDocumentWindow(documentId, type, data) {
    const targetWindow = this.openWindows.get(documentId)
    this.sendToWindow(targetWindow, type, data)
  }

  /**
   * Broadcast message to all open windows
   * @param {string} type - Message type
   * @param {Object} data - Message data
   */
  broadcastToAllWindows(type, data) {
    this.openWindows.forEach((window) => {
      this.sendToWindow(window, type, data)
    })
  }

  /**
   * Set up message listener for communication from child windows
   */
  setupMessageListener() {
    window.addEventListener('message', (event) => {
      // Verify origin for security
      if (event.origin !== window.location.origin) {
        return
      }

      const { type, data, source } = event.data

      // Handle messages from document windows
      if (source === 'document_window') {
        this.handleDocumentWindowMessage(type, data, event.source)
      }
      
      // Handle messages from media windows
      if (source === 'media_window') {
        this.handleMediaWindowMessage(type, data, event.source)
      }
    })
  }

  /**
   * Handle messages from document windows
   * @param {string} type - Message type
   * @param {Object} data - Message data
   * @param {Window} sourceWindow - Source window
   */
  handleDocumentWindowMessage(type, data, sourceWindow) {
    switch (type) {
      case 'DOCUMENT_UPDATED':
        this.notifyDocumentUpdated(data.documentId, data.updates)
        break
      case 'REQUEST_DOCUMENT_DATA':
        this.handleDocumentDataRequest(data.documentId, sourceWindow)
        break
      case 'WINDOW_READY':
        this.handleWindowReady(data.documentId, sourceWindow)
        break
      default:
        console.log('Unknown message from document window:', type, data)
    }
  }

  /**
   * Handle messages from media windows
   * @param {string} type - Message type
   * @param {Object} data - Message data
   * @param {Window} sourceWindow - Source window
   */
  handleMediaWindowMessage(type, data, sourceWindow) {
    switch (type) {
      case 'REQUEST_MEDIA_DATA':
        this.handleMediaDataRequest(data.mediaId, sourceWindow)
        break
      case 'WINDOW_READY':
        this.handleMediaWindowReady(data.mediaId, sourceWindow)
        break
      default:
        console.log('Unknown message from media window:', type, data)
    }
  }

  /**
   * Handle media data request from window (fallback method)
   * @param {number} mediaId - Media ID
   * @param {Window} sourceWindow - Source window
   */
  async handleMediaDataRequest(mediaId, sourceWindow) {
    try {
      console.log('Handling media data request for ID:', mediaId)
      
      // Try to import and use the media store as fallback
      const { useMediaStore } = await import('../stores/media')
      const mediaStore = useMediaStore()
      
      // Get all media and find the one we need
      const allMedia = mediaStore.media
      console.log('Found media in store:', allMedia.length)
      const media = allMedia.find(item => item.id === mediaId)
      
      if (media) {
        // Convert reactive proxy to plain object for postMessage
        const plainMedia = JSON.parse(JSON.stringify(media))
        this.sendToWindow(sourceWindow, 'INIT_MEDIA', { media: plainMedia })
        console.log('Sent fallback media data to window:', plainMedia.filename || plainMedia.label)
      } else {
        console.error('Media not found in store:', mediaId, 'Available media IDs:', allMedia.map(m => m.id))
        // Send error message to window
        this.sendToWindow(sourceWindow, 'MEDIA_ERROR', { 
          error: 'Media not found',
          mediaId: mediaId 
        })
      }
    } catch (error) {
      console.error('Error fetching media data:', error)
      // Send error message to window
      this.sendToWindow(sourceWindow, 'MEDIA_ERROR', { 
        error: error.message,
        mediaId: mediaId 
      })
    }
  }

  /**
   * Handle media window ready notification
   * @param {number} mediaId - Media ID
   * @param {Window} _sourceWindow - Source window (unused, available for future features)
   */
  handleMediaWindowReady(mediaId) {
    console.log(`Media window ready for media ${mediaId}`)
    // Store reference to source window for potential future communication
    // Currently not used but available for future features
  }

  /**
   * Handle document data request from window
   * @param {number} documentId - Document ID
   * @param {Window} sourceWindow - Source window
   */
  async handleDocumentDataRequest(documentId, sourceWindow) {
    try {
      // Import and use the document store
      const { useDocumentStore } = await import('../stores/document')
      const documentStore = useDocumentStore()
      
      // Get all documents and find the one we need
      const allDocuments = documentStore.documents
      const document = allDocuments.find(doc => doc.id === documentId)
      
      if (document) {
        // Convert reactive proxy to plain object for postMessage
        const plainDocument = JSON.parse(JSON.stringify(document))
        this.sendToWindow(sourceWindow, 'DOCUMENT_DATA', { document: plainDocument })
      } else {
        console.error('Document not found:', documentId)
      }
    } catch (error) {
      console.error('Error fetching document data:', error)
    }
  }

  /**
   * Handle window ready notification
   * @param {number} documentId - Document ID
   * @param {Window} sourceWindow - Source window
   */
  handleWindowReady(documentId, sourceWindow) {
    console.log(`Document window ready for document ${documentId}`)
    // Store reference to source window for potential future communication
    // Currently not used but available for future features
    if (sourceWindow) {
      // Could be used for additional window-specific initialization
    }
  }

  /**
   * Notify main app that document was updated in a window
   * @param {number} documentId - Document ID
   * @param {Object} updates - Document updates
   */
  notifyDocumentUpdated(documentId, updates) {
    // Emit event or call callback
    const callbacks = this.windowCallbacks.get('documentUpdated')
    if (callbacks) {
      callbacks.forEach(callback => callback(documentId, updates))
    }
  }

  /**
   * Notify main app that a window was closed
   * @param {number} documentId - Document ID
   */
  notifyWindowClosed(documentId) {
    const callbacks = this.windowCallbacks.get('windowClosed')
    if (callbacks) {
      callbacks.forEach(callback => callback(documentId))
    }
  }

  /**
   * Register callback for window events
   * @param {string} event - Event name
   * @param {Function} callback - Callback function
   */
  on(event, callback) {
    if (!this.windowCallbacks.has(event)) {
      this.windowCallbacks.set(event, [])
    }
    this.windowCallbacks.get(event).push(callback)
  }

  /**
   * Unregister callback for window events
   * @param {string} event - Event name
   * @param {Function} callback - Callback function
   */
  off(event, callback) {
    const callbacks = this.windowCallbacks.get(event)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  /**
   * Check if document has an open window
   * @param {number} documentId - Document ID
   * @returns {boolean}
   */
  hasOpenWindow(documentId) {
    const window = this.openWindows.get(documentId)
    return window && !window.closed
  }

  /**
   * Get all open document IDs
   * @returns {Array<number>}
   */
  getOpenDocumentIds() {
    const openIds = []
    this.openWindows.forEach((window, documentId) => {
      if (!window.closed) {
        openIds.push(documentId)
      }
    })
    return openIds
  }

  /**
   * Close all open windows
   */
  closeAllWindows() {
    this.openWindows.forEach((window) => {
      if (!window.closed) {
        window.close()
      }
    })
    this.openWindows.clear()
  }
}

// Create singleton instance
export const windowManager = new WindowManager()

// Export class for testing
export { WindowManager }