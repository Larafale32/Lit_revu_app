
export function closeModal() {
  const deleteModal = document.querySelector(".deleteModal");
  const button = document.querySelector(".button-non");

  if (!deleteModal || !button) return; // 👈 rien à faire sur cette page

  button.addEventListener("click", () => {
    deleteModal.style.display = "none";
  });
}


export function confirmDelete() {
    const buttons = document.querySelectorAll(".delete-comment-button");
    const deleteModal = document.querySelector(".deleteModal");
    const deleteForm = document.querySelector(".deleteForm");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            console.log("Modal success")
            const commentId = button.dataset.commentId;
            deleteForm.action = `/comment/${commentId}/delete`;
            deleteModal.style.display = "block";
        });
    });
}

// ---- CSRF helper ----
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

export function followButtons(username) {
  const followBtn = document.querySelector(".button_follow");
  const unfollowBtn = document.querySelector(".button_unfollow");
  const followMsg = document.getElementById("followMessage");

  if (followBtn) {
    followBtn.addEventListener("click", () => {
      console.log("follow success")
      sendFollowRequest(username, true, followBtn, unfollowBtn, followMsg);
    });
  }

  if (unfollowBtn) {
    unfollowBtn.addEventListener("click", () => {
      sendFollowRequest(username, false, followBtn, unfollowBtn, followMsg);
    });
  }
}

function sendFollowRequest(username, follow, followBtn, unfollowBtn, followMsg) {
  const url = follow ? `/follow/${username}/` : `/unfollow/${username}/`;

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "X-Requested-With": "XMLHttpRequest"
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        if (follow) {
          followBtn.style.display = "none";
          followMsg.style.display = "block";
          unfollowBtn.style.display = "inline-block";
        } else {
          followBtn.style.display = "inline-block";
          followMsg.style.display = "none";
          unfollowBtn.style.display = "none";
        }
      }
    })
    .catch(err => console.error("Erreur :", err));
}
