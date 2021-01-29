
function editPost(){
    //clear post text and set to empty text area
    const postEditDiv = document.querySelector('#editPostBtn').parentElement;
    const postText = postEditDiv.parentElement.querySelector('.postText');
    const editPostText = postEditDiv.parentElement.querySelector('#editPostInput');
    console.log(editPostText);

    const currentPost = postText.innerHTML.trim();

    postText.innerHTML = "";
    postText.style.display = "none";
    editPostText.style.display = "block";
    editPostText.innerHTML = currentPost;
}

function savePost(){
    const postEditDiv = document.querySelector('#editPostBtn').parentElement;
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

function likePost(post_id){
    fetch(`likePost/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => {
        console.log(response["status"]);
        const likeBtn = document.querySelector('#likeBtn');
        likeBtn.className = "bi bi-heart-fill";
        let numLikes = parseInt(likeBtn.parentElement.innerText);
        numLikes++;
        likeBtn.innerText = numLikes;
    })
    .catch(error => {
        alert("Error liking post.");
    });
}

function unlikePost(post_id){
    fetch(`likePost/${post_id}`, {
        method: 'DELETE',
        body: JSON.stringify({
            post_id: post_id
        })
    })
    .then(response => {
        console.log(response["status"]);
        const likeBtn = document.querySelector('#likeBtn');
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
    console.log(following);
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

function unfollowUser(following){

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
    const editBtn = document.querySelector('#editPostBtn');
    const followBtn = document.querySelector('#followUserBtn');
    const likeBtn = document.querySelector('#likeBtn');

    if(editBtn){
        editBtn.addEventListener('click', () => {
            const editBtnHTML       = editBtn.innerHTML;
            let isEditBtnPressed    = true ? editBtnHTML === 'Edit' :  false;
            
            if(isEditBtnPressed){
                editBtn.innerHTML = 'Save';
                editPost();
            }else{
                savePost();
                editBtn.innerHTML = 'Edit';
            }

        });
    }

    if(followBtn){
        followBtn.addEventListener('click', () => {
            const followBtnHTML = followBtn.innerHTML;
            let following     = document.querySelector('#usernameHeading').dataset.userid;
            let isFollowBtnPressed = true ? followBtnHTML === 'Follow' : false;

            if(isFollowBtnPressed){
                followUser(following);
            }else{
                unfollowUser(following);
            }
        });
    }

    if(likeBtn){
        likeBtn.addEventListener('click', () => {
            const postLikeDiv = likeBtn.parentElement;
            const post        = postLikeDiv.parentElement;
            const postId = parseInt(post.dataset.postid);
            
            
            if(likeBtn.classList.contains('bi-heart-fill')){
                unlikePost(postId);
            }else{
                likePost(postId);
            }
        })
    }

});