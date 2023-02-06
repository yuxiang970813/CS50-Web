function ShowEditPost(id) {
	//? Hide original content
	document.querySelector(`#post-content_${id}`).style.display = 'none';

	//? Show the textarea to let user edit post
	document.querySelector(`#edit-post_${id}`).style.display = 'block';
}

function SaveEditChange(id) {
	editedContent = document.querySelector(`#edit-area_${id}`).value;

	//? Hide the textarea
	document.querySelector(`#edit-post_${id}`).style.display = 'none';

	//? Show the edited content
	document.querySelector(`#contentArea_${id}`).innerHTML = editedContent;
	document.querySelector(`#post-content_${id}`).style.display = 'block';
}

function Unlike(element) {
	//? For later use
	const id = element.dataset.id;

	//* Send like request
	fetch(`/unlike/${element.dataset.id}`)
		.then((response) => response.json())
		.then((result) => {
			console.log(result.message);

			//* Update liker count
			document.querySelector(`#like-count_${id}`).innerHTML =
				result.liker_count;
		});
}

function Like(element) {
	//? For later use
	const id = element.dataset.id;

	//* Send like request
	fetch(`/like/${id}`)
		.then((response) => response.json())
		.then((result) => {
			console.log(result.message);

			//* Update liker count
			document.querySelector(`#like-count_${id}`).innerHTML =
				result.liker_count;
		});
}

//* Liesten for button
document.addEventListener('DOMContentLoaded', () => {
	//* Select all edit button
	document.querySelectorAll('.edit').forEach((edit) => {
		edit.onclick = function () {
			ShowEditPost(this.dataset.id);
		};
	});

	//* Select all save button
	document.querySelectorAll('.save').forEach((save) => {
		save.onclick = function () {
			SaveEditChange(this.dataset.id);
		};
	});

	//* Like/unlike post
	document.addEventListener('click', (event) => {
		//? Find what was clicked on
		const element = event.target;

		//? For use later
		const id = element.dataset.id;
		const likeArea = document.querySelector(`#like-area_${id}`);

		//? Check if the user clicked on a like button
		if (element.className === 'like') {
			//* Request like function & udpate like count
			Like(element);

			//* Remove like button then add unlike button
			element.remove();
			likeArea.innerHTML = `
				<div id="unlike_${id}" class="unlike" data-id="${id}">❤️</div>
			`;
		}

		//? Check if the user clicked on a unlike button
		else if (element.className === 'unlike') {
			//* Request like function & udpate like count
			Unlike(element);

			//* Remove unlike button then add like button
			element.remove();
			likeArea.innerHTML = `
				<div id="like_${id}" class="like" data-id="${id}">🤍</div>
			`;
		}
	});
});
