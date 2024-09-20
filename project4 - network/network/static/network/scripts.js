document.addEventListener("DOMContentLoaded", () => {
    const followButton = document.querySelector(".follow-button")
    if(followButton){
        followButton.addEventListener("click", (event) => {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            const followButton = event.target

            fetch(`/profile/${followButton.dataset.targetid}/follow`, {
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                method: "POST",
                body: ""
            })
            .then(response => response.json())
            .then(result => {
                // Update the button
                if(result.following) {
                    followButton.innerHTML = "Unfollow"
                    followButton.parentNode.querySelector(".follower-count").innerHTML++
                } else {
                    followButton.innerHTML = "Follow"
                    followButton.parentNode.querySelector(".follower-count").innerHTML--
                }
            })
        })
    }

    // Add event listeners to buttons
    try{
        document.querySelectorAll(".like-button").forEach((node) => {
            node.addEventListener("click", event => {
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
                const likeButton = event.target
                // Post to server
                fetch(`/posts/${likeButton.dataset.postid}/like`, {
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "Content-Type": "application/json"
                    },
                    method: "POST",
                    body: ""
                })
                .then(response => response.json())
                .then(result => {
                    // Update the button
                    if(result.liked) {
                        likeButton.innerHTML = "Liked"
                        likeButton.parentNode.querySelector(".like-count").innerHTML++
                    } else {
                        likeButton.innerHTML = "Like"
                        likeButton.parentNode.querySelector(".like-count").innerHTML--
                    }
                })
            })
        })
    } catch {
        // Probably no posts
    }
    
    // Buttons for editing
    try{
        document.querySelectorAll(".post-card").forEach((postCard) => {
            postCard.querySelector(".edit-button").addEventListener("click", event => {
                // Get the form elements
                const editButton = event.target
                const saveButton = editButton.parentNode.querySelector(".save-button")
                const cancelButton = editButton.parentNode.querySelector(".cancel-button")
                const postContent = editButton.parentNode.parentNode.querySelector(".post-content")
                
                // Replace post content with a text area
                const textArea = document.createElement("textarea")
                textArea.innerHTML = postContent.innerHTML
                textArea.classList = postContent.classList
                postContent.parentNode.replaceChild(textArea, postContent)

                // Adjust buttons accordingly
                editButton.hidden = true
                saveButton.hidden = false
                cancelButton.hidden = false
            })
            
            postCard.querySelector(".save-button").addEventListener("click", event => {
                // Get the form elements
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
                const saveButton = event.target
                const cancelButton = saveButton.parentNode.querySelector(".cancel-button")
                const editButton = saveButton.parentNode.querySelector(".edit-button")
                const textArea = saveButton.parentNode.parentNode.querySelector(".post-content")

                // Recreate the postContent element so we can put it back after a save.
                const postContent = document.createElement("p")
                postContent.classList = textArea.classList

                // Post to server
                fetch(`/posts/${saveButton.dataset.postid}/edit`, {
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "Content-Type": "application/json"
                    },
                    method: "POST",
                    body: JSON.stringify({ 
                        "content": textArea.value
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if(result.success){
                        editButton.hidden = false
                        saveButton.hidden = true
                        cancelButton.hidden = true
                        postContent.innerHTML = textArea.value
                        textArea.parentNode.replaceChild(postContent, textArea)
                    } else {
                        const errMsg = document.createElement("span")
                        errMsg.innerHTML = "There was a problem saving"
                        editButton.parentNode.append(errMsg)
                    }
                })
            })

           postCard.querySelector(".cancel-button").addEventListener("click", event => {
                // Get the form elements
                const cancelButton = event.target
                const saveButton = cancelButton.parentNode.querySelector(".save-button")
                const editButton = cancelButton.parentNode.querySelector(".edit-button")
                const textArea = editButton.parentNode.parentNode.querySelector(".post-content")

                // Revert text area to post content
                const postContent = document.createElement("p")
                postContent.classList = textArea.classList
                postContent.innerHTML = textArea.innerHTML
                textArea.parentNode.replaceChild(postContent, textArea)

                // Revert button visibility
                editButton.hidden = false
                saveButton.hidden = true
                cancelButton.hidden = true
            })
        })
    } catch {
        // Probably no posts
    }
})