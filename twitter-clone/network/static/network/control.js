
function editPost(Event){
    //clear post text and set to empty text area
    const postEditDiv = Event.target.parentElement;
    const postText = postEditDiv.parentElement.querySelector('.postText');
    const editPostText = postEditDiv.parentElement.querySelector('#editPostInput');
    

    const currentPost = postText.innerHTML.trim();

    postText.innerHTML = "";
    postText.style.display = "none";
    editPostText.style.display = "block";
    editPostText.innerHTML = currentPost;
}

function savePost(Event){
    const postEditDiv = Event.target.parentElement;
    const post = postEditDiv.parentElement;
    const postId = parseInt(post.dataset.postid);
    const postText = postEditDiv.parentElement.querySelector('.postText');
    const editPostText = postEditDiv.parentElement.querySelector('#editPostInput');

    const newPost = editPostText.value;

    fetch(`/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: newPost
        })
    })
    .then(response => {
        console.log(response["status"]);
    })
    .catch(() => {
        alert("Error saving post");
    });
    
    postText.innerHTML = newPost;
    editPostText.innerHTML = "";
    postText.style.display = "block";
    editPostText.style.display = "none";
}

function likePost(Event, post_id){
    fetch(`likePost/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => {
        console.log(response["status"]);
        const likeBtn = Event.target;
        likeBtn.className = "bi bi-heart-fill";
        let numLikes = parseInt(likeBtn.parentElement.innerText);
        numLikes++;
        likeBtn.innerText = numLikes;
    })
    .catch(error => {
        alert("Error liking post.");
    });
}

function unlikePost(Event, post_id){
    fetch(`likePost/${post_id}`, {
        method: 'DELETE',
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => {
        console.log(response["status"]);
        const likeBtn = Event.target;
        let numLikes = parseInt(likeBtn.parentElement.innerText);
        likeBtn.className = "bi bi-heart";
        numLikes--;
        likeBtn.innerText = numLikes;
    })
    .catch(error => {
        alert("Error liking post.");
    });
}

function followUser(following){
    fetch(`followUser/`, {
        method: 'PUT',
        body: JSON.stringify({
            isFollowing: false,
            following_user: following
        })
    })
    .then(response => {
        console.log(response["status"]);
        const followBtn = document.querySelector('#followUserBtn');
        followBtn.innerHTML = 'Unfollow';
    })
    .catch(error => {
        alert("Error following user.");
    });
}

function unfollowUser( following){

    fetch(`followUser/`, {
        method: 'DELETE',
        body: JSON.stringify({
            isFollowing: true,
            following_user: following
        })
    })
    .then(response => {
        console.log(response["status"]);
        const followBtn = document.querySelector('#followUserBtn');
        followBtn.innerHTML = 'Follow';
    })
    .catch(error => {
        alert("Error following user.");
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.querySelectorAll('#editPostBtn');
    const followBtn = document.querySelector('#followUserBtn');
    const likeBtn = document.querySelectorAll('#likeBtn');

    if(editBtn.length > 0){
        editBtn.forEach(eBtn => {
            eBtn.addEventListener('click', (Event) => {
                const editBtnHTML       = eBtn.innerHTML;
                let isEditBtnPressed    = true ? editBtnHTML === 'Edit' :  false;
                
                if(isEditBtnPressed){
                    eBtn.innerHTML = 'Save';
                    editPost(Event);
                }else{
                    savePost(Event);
                    eBtn.innerHTML = 'Edit';
                }
            });
        })
    }

    if(followBtn){

        followBtn.addEventListener('click', (Event) => {
            const followBtnHTML = followBtn.innerHTML;
            let following     = document.querySelector('#usernameHeading').dataset.userid;
            let isFollowBtnPressed = true ? followBtnHTML === 'Follow' : false;

            if(isFollowBtnPressed){
                followUser(Event, following);
            }else{
                unfollowUser(Event, following);
            }
        });
    }

    if(likeBtn.length > 0){
        likeBtn.forEach(lkBtn => {
            lkBtn.addEventListener('click', (Event) => {
                const postLikeDiv = lkBtn.parentElement;
                const post        = postLikeDiv.parentElement;
                const postId = parseInt(post.dataset.postid);
                
                
                if(lkBtn.classList.contains('bi-heart-fill')){
                    unlikePost(Event, postId);
                }else{
                    likePost(Event, postId);
                }
            });
        });
        
    }

});