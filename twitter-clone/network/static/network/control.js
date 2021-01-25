
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

function likePost(){

}

document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.querySelector('#editPostBtn');

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

    })
});