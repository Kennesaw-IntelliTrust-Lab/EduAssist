// JS FOR DASHBOARD

document.addEventListener('DOMContentLoaded', function() {
    // Helper function to get CSRF token - moved to the top since it's used by multiple features
    function getCSRFToken() {
        const csrfCookie = document.cookie
            .split(';')
            .find(cookie => cookie.trim().startsWith('csrftoken='));
        return csrfCookie ? csrfCookie.split('=')[1] : '';
    }
    
    // Course management functionality
    const addCourseBtn = document.getElementById('add-course-btn');
    const addCourseModal = document.getElementById('add-course-modal');
    const saveCourseBtn = document.getElementById('save-course-btn');
    const courseForm = document.getElementById('course-form');
    const courseNameInput = document.getElementById('id_name');
    const courseError = document.getElementById('course-error');
// Initialize Bootstrap modal
let courseModal;
if (addCourseModal) {
    courseModal = new bootstrap.Modal(addCourseModal);
    
    // Add event listeners for close buttons
    const closeButtons = addCourseModal.querySelectorAll('[data-bs-dismiss="modal"]');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            courseModal.hide();
        });
    });
}


// Show course modal when add course button is clicked
if (addCourseBtn) {
    addCourseBtn.addEventListener('click', function() {
        if (courseNameInput) {
            courseNameInput.value = '';
        }
        if (courseError) {
            courseError.style.display = 'none';
            courseError.textContent = '';
        }
        
        if (courseModal) {
            courseModal.show();
        }
    });
}

// Save course when button is clicked   

if (saveCourseBtn) {
    saveCourseBtn.addEventListener('click', function() {
        if (!courseNameInput || !courseNameInput.value.trim()) {
            courseError.textContent = 'Please enter a course name';
            courseError.style.display = 'block';
            return;
        }
        
        const courseName = courseNameInput.value.trim();
        
        // Create FormData object instead of JSON
        const formData = new FormData();
        formData.append('name', courseName);
        
        fetch('/api/add-course/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                courseError.textContent = typeof data.error === 'string' ? data.error : 'Failed to add course';
                courseError.style.display = 'block';
                return;
            }
            
            // Hide modal and refresh page to show new course
            courseModal.hide();
            window.location.href = `?course=${data.id}`;
        })
        .catch(error => {
            console.error('Error adding course:', error);
            courseError.textContent = 'An error occurred. Please try again.';
            courseError.style.display = 'block';
        });
    });
}
    // Allow Enter key to submit the course form
    if (courseNameInput) {
        courseNameInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                saveCourseBtn.click();
            }
        });
    }

    // File upload functionality
    const fileInput = document.getElementById('id_file');
    const fileDropArea = document.getElementById('file-drop-area');
    const fileNameDisplay = document.getElementById('selected-file-name');
    
    if (fileDropArea && fileInput) {
        fileDropArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
                fileDropArea.style.borderColor = '#4361ee';
            } else {
                fileNameDisplay.textContent = 'No file chosen';
                fileDropArea.style.borderColor = '#ced4da';
            }
        });
        
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            fileDropArea.style.borderColor = '#4361ee';
            fileDropArea.style.backgroundColor = 'rgba(67, 97, 238, 0.05)';
        }
        
        function unhighlight() {
            fileDropArea.style.borderColor = '#ced4da';
            fileDropArea.style.backgroundColor = 'transparent';
        }
        
        fileDropArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            
            if (files.length > 0) {
                fileNameDisplay.textContent = files[0].name;
            }
        }
    }

    // Global variable to store currently selected chat files
    window.selectedChatFiles = [];

    // Function to handle file generation
    function generateFile(content, filename) {
        // Get selected course if exists
        const urlParams = new URLSearchParams(window.location.search);
        const courseId = urlParams.get('course');
        
        fetch('/api/generate-file/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                content: content,
                file_name: filename,
                file_type: getFileTypeFromName(filename),
                course_id: courseId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error generating file:', data.error);
                return;
            }
            
            // Create download link for the generated file
            const downloadDiv = document.createElement('div');
            downloadDiv.className = 'generated-file-download';
            downloadDiv.innerHTML = `
                <div class="file-download-icon"><i class="fas fa-file-download"></i></div>
                <div class="file-download-info">
                    <span>Generated file: ${data.file_name.split('/').pop()}</span>
                    <a href="${data.file_url}" target="_blank" class="download-link">
                        <i class="fas fa-download"></i> Download
                    </a>
                </div>
            `;
            
            // Add to the last bot message
            const botMessages = document.querySelectorAll('.bot-message');
            const lastBotMessage = botMessages[botMessages.length - 1];
            lastBotMessage.appendChild(downloadDiv);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Helper function to get file type from filename
    function getFileTypeFromName(filename) {
        const parts = filename.split('.');
        if (parts.length > 1) {
            const extension = parts[parts.length - 1].toLowerCase();
            // Only allow text-based formats
            if (['txt', 'md', 'csv'].includes(extension)) {
                return extension;
            }
        }
        return 'txt'; // Default to txt
    }

    // Chatbot functionality
    const chatIcon = document.getElementById("chatbot-icon");
    const chatWindow = document.getElementById("chatbot-window");
    const chatClose = document.getElementById("chatbot-close");
    const chatInput = document.getElementById("chatbot-user-input");
    const chatSend = document.getElementById("chatbot-send");
    const messagesDiv = document.getElementById("chatbot-messages");
    const chatFileInput = document.getElementById("chat-file-input");
    const chatAttachButton = document.getElementById("chatbot-attach-file");

    // Load chat history function
    function loadChatHistory() {
        fetch('/api/chat-history/')
            .then(response => response.json())
            .then(data => {
                // Clear existing messages
                messagesDiv.innerHTML = '';
                
                // Add welcome message
                const welcomeMessage = document.createElement("div");
                welcomeMessage.className = "bot-message";
                welcomeMessage.textContent = "Hello! I'm your EduAssist chatbot. How can I help you today with your coursework?";
                messagesDiv.appendChild(welcomeMessage);
                
                // Add chat history
                if (data.chats && data.chats.length > 0) {
                    data.chats.reverse().forEach(chat => {
                        // Add user message
                        const userMessageDiv = document.createElement("div");
                        userMessageDiv.className = "user-message";
                        userMessageDiv.textContent = chat.message;
                        messagesDiv.appendChild(userMessageDiv);
                        
                        // Add bot response
                        const botMessageDiv = document.createElement("div");
                        botMessageDiv.className = "bot-message";
                        botMessageDiv.textContent = chat.response;
                        messagesDiv.appendChild(botMessageDiv);
                    });
                }
                
                // Scroll to bottom
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            })
            .catch(error => {
                console.error('Error loading chat history:', error);
            });
    }

// Add event handler for logout button - using class and text content to identify it
const logoutButton = document.querySelector('a.nav-link[href*="logout"]');
if (logoutButton) {
    logoutButton.addEventListener('click', function(e) {
        // Only prevent default if we can show the confirmation
        if (!confirm('Logging out will delete all files uploaded to or generated by the chatbot. Continue?')) {
            e.preventDefault(); // Only prevent logout if user clicks Cancel
        }
        // If confirmed, let the default link behavior happen naturally
    });
}

    // Function to handle file upload for chat
function uploadChatFile() {
    const files = chatFileInput.files;
    const errorElement = document.getElementById('file-upload-error');
    
    // Reset error message
    if (errorElement) {
        errorElement.style.display = 'none';
        errorElement.textContent = '';
    }
    
    if (files.length === 0) {
        return;
    }
    
    const file = files[0];
    
    // Check file type (same as server-side check)
    const allowedTypes = ['.txt', '.csv', '.md', '.pdf', '.docx', '.xlsx', '.pptx', '.jpg', '.jpeg', '.png'];
    const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    // Log file information for debugging
    console.log("File upload attempt:", {
        name: file.name,
        extension: fileExt,
        type: file.type,
        size: file.size
    });
    
    // Fixed logic for file type checking
    if (!allowedTypes.includes(fileExt)) {
        if (errorElement) {
            errorElement.textContent = `File type ${fileExt} is not supported. Supported types: ${allowedTypes.join(', ')}`;
            errorElement.style.display = 'block';
        }
        chatFileInput.value = '';
        return;
    }
    
    // Special handling for image files - now outside the previous check
    if (['.jpg', '.jpeg', '.png'].includes(fileExt)) {
        console.log("Processing image file:", file.name, file.type);
    }
    
    // Check file size (5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        if (errorElement) {
            errorElement.textContent = 'File size exceeds the maximum limit of 5MB';
            errorElement.style.display = 'block';
        }
        chatFileInput.value = '';
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading indicator
    const loadingEl = document.createElement('div');
    loadingEl.className = 'selected-file';
    loadingEl.innerHTML = `<span>${file.name} (Uploading...)</span>`;
    const selectedFilesEl = document.getElementById('selected-chat-files');
    if (selectedFilesEl) {
        selectedFilesEl.appendChild(loadingEl);
    }
    
    fetch('/api/upload-chat-file/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        body: formData
    })
    .then(response => {
        // Log raw response for debugging
        console.log("File upload response status:", response.status);
        return response.json();
    })
    .then(data => {
        // Remove loading indicator
        if (selectedFilesEl && loadingEl) {
            selectedFilesEl.removeChild(loadingEl);
        }
        
        // Log response data for debugging
        console.log("File upload response data:", data);
        
        if (data.error) {
            if (errorElement) {
                errorElement.textContent = data.error;
                errorElement.style.display = 'block';
            }
            return;
        }
        
        // Add file to selected files array
        window.selectedChatFiles.push({
            id: data.file_id,
            name: data.file_name
        });
        
        // Display selected file in UI
        displaySelectedChatFiles();
        
        // Clear file input
        chatFileInput.value = '';
    })
    .catch(error => {
        // Remove loading indicator
        if (selectedFilesEl && loadingEl) {
            selectedFilesEl.removeChild(loadingEl);
        }
        
        console.error('Error uploading file:', error);
        
        if (errorElement) {
            errorElement.textContent = 'Error uploading file. Please try again.';
            errorElement.style.display = 'block';
        }
        chatFileInput.value = '';
    });
}

    // Function to display selected files in the chat UI
    function displaySelectedChatFiles() {
        const fileListElement = document.getElementById('selected-chat-files');
        if (!fileListElement) return;
        
        fileListElement.innerHTML = '';
        
        window.selectedChatFiles.forEach(file => {
            // Get file extension to show appropriate icon
            const fileName = file.name.split('/').pop(); // Get just the filename
            const fileExt = fileName.substring(fileName.lastIndexOf('.')).toLowerCase();
            let iconClass = 'fas fa-file';
            
            // Assign icon based on file type
            if (fileExt === '.pdf') {
                iconClass = 'fas fa-file-pdf file-type-pdf';
            } else if (fileExt === '.docx') {
                iconClass = 'fas fa-file-word file-type-doc';
            } else if (fileExt === '.xlsx') {
                iconClass = 'fas fa-file-excel file-type-xls';
            } else if (fileExt === '.txt' || fileExt === '.md' || fileExt === '.csv') {
                iconClass = 'fas fa-file-alt file-type-txt';
            } else if (fileExt === '.jpg' || fileExt === '.jpeg' || fileExt === '.png') {
                iconClass = 'fas fa-file-image';
            }
            
            const fileElement = document.createElement('div');
            fileElement.className = 'selected-file';
            fileElement.innerHTML = `
                <i class="${iconClass} file-type-icon"></i>
                <span>${fileName}</span>
                <button type="button" data-file-id="${file.id}">✕</button>
            `;
            
            // Add click event for remove button
            const removeBtn = fileElement.querySelector('button');
            if (removeBtn) {
                removeBtn.addEventListener('click', function() {
                    const fileId = parseInt(this.getAttribute('data-file-id'));
                    removeSelectedFile(fileId);
                });
            }
            
            fileListElement.appendChild(fileElement);
        });
    }

    // Function to remove a selected file
    function removeSelectedFile(fileId) {
        window.selectedChatFiles = window.selectedChatFiles.filter(file => file.id !== fileId);
        displaySelectedChatFiles();
    }

    // Send message function with file generation support
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message === "") return;

        // Get file IDs from selected files
        const fileIds = window.selectedChatFiles.map(file => file.id);

        // Add user message to chat
        const userMessageDiv = document.createElement("div");
        userMessageDiv.className = "user-message";
        
        // Create message content with file attachments if any
        let messageContent = message;
        if (window.selectedChatFiles.length > 0) {
            messageContent += `<div class="attached-files">
                <i class="fas fa-paperclip"></i> ${window.selectedChatFiles.length} file(s) attached
            </div>`;
        }
        
        userMessageDiv.innerHTML = messageContent;
        messagesDiv.appendChild(userMessageDiv);

        // Clear input
        chatInput.value = "";

        // Scroll to bottom
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Show typing indicator
        const typingIndicator = document.createElement("div");
        typingIndicator.className = "typing-indicator bot-message";
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        messagesDiv.appendChild(typingIndicator);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Send to backend and get response
        fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ 
                message: message,
                file_ids: fileIds
            })
        })
        .then(response => response.json())
        .then(data => {
            messagesDiv.removeChild(typingIndicator);

            // Add bot response
            const botMessageDiv = document.createElement("div");
            botMessageDiv.className = "bot-message";
            
            // Format response with line breaks
            botMessageDiv.innerHTML = data.response.replace(/\n/g, '<br>');
            messagesDiv.appendChild(botMessageDiv);

            // Check if file generation data is included
            if (data.file_generation) {
                generateFile(data.file_generation.content, data.file_generation.filename);
            }

            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            // Clear selected files after sending
            window.selectedChatFiles = [];
            displaySelectedChatFiles();
        })
        .catch(error => {
            messagesDiv.removeChild(typingIndicator);

            const errorMessageDiv = document.createElement("div");
            errorMessageDiv.className = "bot-message";
            errorMessageDiv.textContent = "Sorry, I'm having trouble connecting right now. Please try again later.";
            messagesDiv.appendChild(errorMessageDiv);

            console.error('Error:', error);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        });
    }

    // Chatbot event listeners
    if (chatIcon) {
        chatIcon.addEventListener("click", function() {
            chatWindow.style.display = chatWindow.style.display === "flex" ? "none" : "flex";
            if (chatWindow.style.display === "flex") {
                loadChatHistory();
                setTimeout(() => {
                    chatInput.focus();
                }, 100);
            }
        });
    }

    if (chatClose) {
        chatClose.addEventListener("click", function() {
            chatWindow.style.display = "none";
        });
    }

    if (chatSend) {
        chatSend.addEventListener("click", sendMessage);
    }

    if (chatInput) {
        chatInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }
    
    // Add file upload event listeners
    if (chatFileInput) {
        chatFileInput.addEventListener('change', uploadChatFile);
    }
    
    if (chatAttachButton) {
        chatAttachButton.addEventListener('click', function() {
            chatFileInput.click();
        });
    }

    // Tab activation persistence with localStorage
    const tabLinks = document.querySelectorAll('.nav-tabs .nav-link');
    
    // Set active tab based on localStorage or default to first tab
    const activeTab = localStorage.getItem('activeTab') || '#assignments';
    const tabToActivate = document.querySelector(`[href="${activeTab}"]`);
    if (tabToActivate) {
        const tab = new bootstrap.Tab(tabToActivate);
        tab.show();
    }
    
    // Store active tab in localStorage when changed
    if (tabLinks) {
        tabLinks.forEach(link => {
            link.addEventListener('shown.bs.tab', function(e) {
                localStorage.setItem('activeTab', e.target.getAttribute('href'));
            });
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggerList.length > 0) {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Delete file functionality
    const deleteButtons = document.querySelectorAll('.delete-file');
    
    if (deleteButtons) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const fileId = this.getAttribute('data-file-id');
                
                if (confirm('Are you sure you want to delete this file?')) {
                    fetch(`/delete-file/${fileId}/`, {
                        method: 'POST',  // Using POST since some browsers don't support DELETE with fetch
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message) {
                            // Remove the file item from the UI
                            this.closest('.file-item').remove();
                        } else {
                            alert('Failed to delete the file: ' + (data.error || 'Unknown error'));
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while deleting the file.');
                    });
                }
            });
        });
    }
});