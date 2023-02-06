document.addEventListener('DOMContentLoaded', function () {
  //* Use buttons to toggle between views
  document
    .querySelector('#inbox')
    .addEventListener('click', () => load_mailbox('inbox'));

  document
    .querySelector('#sent')
    .addEventListener('click', () => load_mailbox('sent'));

  document
    .querySelector('#archived')
    .addEventListener('click', () => load_mailbox('archive'));

  document
    .querySelector('#compose')
    .addEventListener('click', () => compose_email());

  //* By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(content) {
  //? Select the submit button and inputs to be used later
  const form = document.querySelector('#compose-form');
  const recipients = document.querySelector('#compose-recipients');
  const subject = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body');
  const submit = document.querySelector('#compose-submit');

  //* Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  //* Clear out composition fields
  //! Compose button been clicked
  if (content === undefined) {
    //? Clear all composition fields
    recipients.value = '';
    body.value = '';
    subject.value = '';
  }
  //! Reply button been clicked
  else {
    //? Pre-fill the composition form of the original email
    recipients.value = content.sender;
    body.value = `On ${content.timestamp} ${content.sender} wrote: ${content.body}`;

    //? For later use
    const subjectLine = content.subject;

    //! Subject line already begins with 'Re: '
    if (subjectLine.slice(0, 4) === 'Re: ') {
      //? Just pre-fill current subject line
      subject.value = `${subjectLine}`;
    }

    //! First time reply
    else {
      //? Add 'Re :' to subject line
      subject.value = `Re: ${subjectLine}`;
    }
  }

  //! Disable submit button by default:
  submit.disabled = true;

  //* Listen for input to be typed into the subject field
  form.onkeyup = () => {
    //? Disable submit if no word in subject & body
    if (subject.value.length > 0 && body.value.length > 0) {
      submit.disabled = false;
    }

    //? Enable submit if has word in subject & body
    else {
      submit.disabled = true;
    }
  };

  //* Listen for submission of form
  form.onsubmit = () => {
    //? Send email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients.value,
        subject: subject.value,
        body: body.value,
      }),
    })
      //? Put response into json form
      .then((response) => response.json())

      .then((result) => {
        //* Load the user’s sent mailbox if email sent successfully
        if (result.error === undefined) {
          alert(result.message);
          load_mailbox('sent');
        }

        //! Alert error message
        else {
          alert(result.error);
        }
      });

    //! Stop form from submission
    return false;
  };
}

function load_mailbox(mailbox) {
  //? Select elements to be used later
  const emailView = document.querySelector('#emails-view');
  const contentView = document.querySelector('#content-view');
  const composeView = document.querySelector('#compose-view');

  //! Show the mailbox and hide other views
  composeView.style.display = 'none';
  contentView.style.display = 'none';
  emailView.style.display = 'block';

  //! Show the mailbox name
  emailView.innerHTML = `
    <h3>
      ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}
    </h3>
  `;

  //* Load mailbox
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())

    .then((emails) => {
      emails.forEach(addBox);
    });

  //* Add new box with given contents to DOM
  function addBox(email) {
    //? Assign contents into box
    const box = document.createElement('div');

    box.className = 'd-flex border rounded';

    box.innerHTML = `
      <div class="p-2 font-weight-bold">
        ${email.sender}
      </div>
      <div class="p-2">
        ${email.subject}
      </div>
      <div class="ml-auto p-2 text-muted">
        ${email.timestamp}
      </div>
    `;

    //* Show mail content when been clicked
    box.addEventListener('click', () => {
      view_email(email.id);
    });

    //* Add box to DOM
    emailView.append(box);

    //* Indicate read/unread with background color
    //? Grey when read
    if (email.read) {
      box.style.background = 'LightGrey';
    }

    //? White when unread
    else {
      box.style.background = 'white';
    }
  }
  
  //* View email content
  function view_email(email_id) {
    //? Reset content view
    contentView.innerHTML = '';

    //? Show mail content view and hide other views
    composeView.style.display = 'none';
    emailView.style.display = 'none';
    contentView.style.display = 'block';

    //? Request email content
    fetch(`/emails/${email_id}`)
      .then((response) => response.json())

      .then((content) => {
        //? Create archive/unarchive button & area for content
        const archiveButton = document.createElement('div');
        const mailContent = document.createElement('div');

        //? Assign class to archiveButton
        archiveButton.className = 'text-right';

        //! User already archived this email
        if (content.archived) {
          archiveButton.innerHTML = `
            <button id="archive" class="btn btn-primary btn-sm">
              Unarchive
            </button>
          `;
        }

        //! User haven't archived this email
        else {
          archiveButton.innerHTML = `
            <button id="archive" class="btn btn-primary btn-sm">
              Archive
            </button>
          `;
        }

        //? Put content inside content area
        mailContent.innerHTML = `
          <p>
            <strong>From:</strong>
            ${content.sender}
          </p>
          <p>
            <strong>To:</strong>
            ${content.recipients}
          </p>
          <p>
            <strong>Subject:</strong>
            ${content.subject}
          </p>
          <p>
            <strong>Timestamp:</strong>
            ${content.timestamp}
          </p>
          <input type="submit" value="Reply" id="reply-email" class="btn btn-info btn-sm">
          <hr>
          <p>
            ${content.body}
          </p>
        `;

        //* Make unread email read
        if (!content.read) {
          fetch(`/emails/${content.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true,
            }),
          });
        }

        //! Don't apply archive/unarchive button to Sent mailbox
        if (mailbox === 'sent') {
          //? Mail content only
          contentView.append(mailContent);
        }

        //* Other mailbox have both button and content
        else {
          //? Both
          contentView.append(mailContent, archiveButton);

          //? Listen and toggle archive/unarchive button
          document.querySelector('#archive').addEventListener('click', () => {
            assignArchive(content);
          });
        }

        //* Listen to reply button
        document.querySelector('#reply-email').addEventListener('click', () => {
          compose_email(content);
        });
      });
  }

  //! Prevent default submission
  return false;
}

function assignArchive(mail) {
  //! Click to unarchive
  if (mail.archived) {
    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false,
      }),
    });

    //?
    alert('Unarchive successfully!');
  }

  //! Click to archive
  else {
    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true,
      }),
    });

    //?
    alert('Archive successfully!');
  }

  //* Redirect to inbox
  load_mailbox('inbox');
}
