// Global variables
let currentSessionId = null;
let isProcessing = false;

// DOM elements
const uploadSection = document.getElementById('uploadSection');
const chatSection = document.getElementById('chatSection');
const uploadArea = document.getElementById('uploadArea');
const pdfFileInput = document.getElementById('pdfFile');
const loadingOverlay = document.getElementById('loadingOverlay');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendMessage');
const typingIndicator = document.getElementById('typingIndicator');
const currentFileName = document.getElementById('currentFileName');
const chunkCount = document.getElementById('chunkCount');
const uploadNewBtn = document.getElementById('uploadNew');
const clearSessionBtn = document.getElementById('clearSession');
const suggestions = document.querySelectorAll('.suggestion');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupAutoResize();
    setupDragAndDrop();
});

// Initialize all event listeners
function initializeEventListeners() {
    // File upload
    uploadArea.addEventListener('click', () => pdfFileInput.click());
    pdfFileInput.addEventListener('change', handleFileSelect);
    
    // Chat functionality
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', handleKeyPress);
    
    // Navigation
    uploadNewBtn.addEventListener('click', showUploadSection);
    clearSessionBtn.addEventListener('click', clearSession);
    
    // Suggestions
    suggestions.forEach(suggestion => {
        suggestion.addEventListener('click', () => {
            messageInput.value = suggestion.dataset.suggestion;
            messageInput.focus();
        });
    });
}

// Setup drag and drop functionality
function setupDragAndDrop() {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type === 'application/pdf') {
            handleFileUpload(files[0]);
        } else {
            showNotification('Please select a valid book PDF file', 'error');
        }
    });
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
}

// Handle file upload
async function handleFileUpload(file) {
    if (!file.type.includes('pdf')) {
        showNotification('Please select a valid book PDF file', 'error');
        return;
    }
    
    showLoadingOverlay();
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload-pdf', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentSessionId = data.session_id;
            currentFileName.textContent = data.filename;
            chunkCount.textContent = `${data.chunk_count} chapters loaded`;
            
            showChatSection();
            showNotification(`"${data.filename}" uploaded successfully! Ready for spoiler-free discussions.`, 'success');
        } else {
            showNotification(data.error || 'Failed to upload book', 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('Network error. Please try again.', 'error');
    } finally {
        hideLoadingOverlay();
    }
}

// Show chat section
function showChatSection() {
    uploadSection.style.display = 'none';
    chatSection.style.display = 'flex';
    chatSection.style.flexDirection = 'column';
    
    // Scroll to bottom of messages
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Show upload section
function showUploadSection() {
    chatSection.style.display = 'none';
    uploadSection.style.display = 'flex';
    
    // Clear current session
    currentSessionId = null;
    currentFileName.textContent = 'Your Book.pdf';
    chunkCount.textContent = '0 chapters loaded';
    
    // Clear chat messages except welcome
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    chatMessages.innerHTML = '';
    chatMessages.appendChild(welcomeMessage);
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isProcessing) return;
    
    if (!currentSessionId) {
        showNotification('Please upload a book first', 'error');
        return;
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    resizeTextarea();
    
    // Show typing indicator
    showTypingIndicator();
    isProcessing = true;
    sendButton.disabled = true;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: currentSessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Add AI response to chat
            addMessage(data.response, 'ai');
        } else {
            addMessage('Sorry, I encountered an error while reading your book. Please try again.', 'ai');
            console.error('Chat error:', data.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        addMessage('Network error. Please check your connection and try again.', 'ai');
    } finally {
        hideTypingIndicator();
        isProcessing = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

// Add message to chat
function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-book-open"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = `<p>${content}</p>`;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageContent.appendChild(bubble);
    messageContent.appendChild(time);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Handle key press
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// Setup auto-resize for textarea
function setupAutoResize() {
    messageInput.addEventListener('input', resizeTextarea);
}

function resizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// Show/hide loading overlay
function showLoadingOverlay() {
    loadingOverlay.style.display = 'flex';
}

function hideLoadingOverlay() {
    loadingOverlay.style.display = 'none';
}

// Show/hide typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Clear session
async function clearSession() {
    if (currentSessionId) {
        try {
            await fetch('/api/clear-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: currentSessionId
                })
            });
        } catch (error) {
            console.error('Error clearing session:', error);
        }
    }
    
    showUploadSection();
    showNotification('Book session cleared', 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #4CAF50, #45a049)' : 
                     type === 'error' ? 'linear-gradient(135deg, #f44336, #d32f2f)' : 
                     'linear-gradient(135deg, #8b5cf6, #7c3aed)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        z-index: 3000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
    `;
    
    notification.querySelector('.notification-content').style.cssText = `
        display: flex;
        align-items: center;
        gap: 0.5rem;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add some visual effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to upload area
    uploadArea.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02)';
    });
    
    uploadArea.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
    
    // Add pulse effect to send button when typing
    messageInput.addEventListener('input', function() {
        if (this.value.trim()) {
            sendButton.style.animation = 'pulse 1s ease-in-out infinite';
        } else {
            sendButton.style.animation = 'none';
        }
    });
    
    // Add CSS for pulse animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    `;
    document.head.appendChild(style);
});

// Handle window resize
window.addEventListener('resize', function() {
    resizeTextarea();
});

// Add smooth scrolling to chat messages
function smoothScrollToBottom(element) {
    element.scrollTo({
        top: element.scrollHeight,
        behavior: 'smooth'
    });
}

// Enhance message animations
function enhanceMessageAnimation(messageElement) {
    messageElement.style.opacity = '0';
    messageElement.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        messageElement.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        messageElement.style.opacity = '1';
        messageElement.style.transform = 'translateY(0)';
    }, 100);
}

// Add this to the addMessage function
const originalAddMessage = addMessage;
addMessage = function(content, sender) {
    originalAddMessage(content, sender);
    
    // Enhance the last message
    const lastMessage = chatMessages.lastElementChild;
    if (lastMessage) {
        enhanceMessageAnimation(lastMessage);
    }
}; 