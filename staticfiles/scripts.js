const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const chatSocket = new WebSocket(
    wsProtocol + '://' + window.location.host + '/ws/comments/'
);


chatSocket.onopen = function() {
    console.log('WebSocket connected');
};

chatSocket.onclose = function(e) {
    console.error('WebSocket closed unspecified::', e);
};

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
