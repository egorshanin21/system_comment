/**
 * Establishes a WebSocket connection to the server for receiving real-time comments.
 * The WebSocket URL is determined based on the current protocol (https or http).
 * If the connection is successful, it listens for incoming messages from the server.
 *
 * The connection is established using either 'wss' (WebSocket Secure) for HTTPS or 'ws' for HTTP.
 * The WebSocket is connected to the '/ws/comments/' endpoint on the current host.
 */
const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const chatSocket = new WebSocket(
    wsProtocol + '://' + window.location.host + '/ws/comments/'
);
/**
 * Handler for when the WebSocket connection is successfully opened.
 * Logs a message to the console indicating that the WebSocket has connected.
 */
chatSocket.onopen = function() {
    console.log('WebSocket connected');
};
/**
 * Handler for when the WebSocket connection is closed.
 * Logs an error message to the console if the WebSocket connection is closed unexpectedly.
 *
 * @param {Event} e - The event object containing information about the closure of the WebSocket connection.
 */
chatSocket.onclose = function(e) {
    console.error('WebSocket closed unspecified::', e);
};
/**
 * Handler for receiving messages from the WebSocket.
 * When a message is received, it attempts to parse the message data and logs it to the console.
 * If the message type is 'new_comment', it processes the comment data by calling the `addCommentToList` function.
 *
 * @param {MessageEvent} e - The event object containing the received WebSocket message.
 */
chatSocket.onmessage = function(e) {
    console.log('Received message from server:', e.data);
    try {
        const data = JSON.parse(e.data);


        console.log('Parsed data:', data);

        if (data.type === 'new_comment') {
            const commentData = data.comment_data;
            console.log('Processing a new comment:', commentData);
            addCommentToList(commentData);
        }
    } catch (error) {
        console.error('Error parsing message:', error);
    }
};
/**
 * Adds a new comment to the list of comments on the page.
 * Creates a new list item with the comment data and appends it to the appropriate place in the comment list.
 *
 * If the comment is a reply to another comment, it finds the parent comment and appends the new comment as a reply.
 * If no parent comment is found, the new comment is added to the top-level comment list.
 *
 * @param {Object} commentData - The data for the new comment, including username, email, text, and other metadata.
 */
function addCommentToList(commentData) {
    const commentsList = document.querySelector("ul");
    const newComment = document.createElement("li");
    newComment.innerHTML = `
        <strong>${commentData.username}</strong> (${commentData.email}) - ${commentData.created_at}:
        <p>${commentData.text}</p>
        <a href="/add-comment/${commentData.id}/" class="btn-custom btn-narrow">Reply</a>
    `;

    newComment.setAttribute('data-comment-id', commentData.id);

    if (commentData.parent_id) {
        const parentComment = commentsList.querySelector(`li a[href="/add-comment/${commentData.parent_id}/"]`);
        console.log('\n' +
            'Find parent comment by URL:', commentData.parent_id);
        if (parentComment) {
            const parentListItem = parentComment.closest("li");
            console.log('Parent comment found:', commentData.parent_id);

            let repliesList = parentListItem.querySelector("ul");
            if (!repliesList) {
                repliesList = document.createElement("ul");
                parentListItem.appendChild(repliesList);
            }
            repliesList.appendChild(newComment);
        } else {
            console.error('No parent comment found:', commentData.parent_id);
            commentsList.prepend(newComment);
        }
    } else {
        commentsList.prepend(newComment);
    }
}
