
  var quill = new Quill("#editor", {
    theme: "snow",
    placeholder: "متن پست خود را اینجا بنویسید...",
    modules: {
      toolbar: [
        ["bold", "italic"],
        ["link"],
        [{ list: "ordered" }, { list: "bullet" }],
        ["blockquote", "code-block"],
        ["clean"],
      ],
    },
  });

  const form = document.getElementById("postForm");
  const hiddenInput = document.getElementById("hiddenContent");
  const editorError = document.getElementById("editorError");

  form.addEventListener("submit", function (e) {
    const content = quill.getText().trim();

    if (content.length === 0) {
      e.preventDefault();
      editorError.classList.remove("d-none");
      return;
    }

    hiddenInput.value = quill.root.innerHTML;
  });
