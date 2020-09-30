<template>
  <div class="editor">
    <editor-menu-bar class="manubar" :editor="editor" v-slot="{ commands }">
      <div class="menubar">
        <button class="menubar__button" @click="showImagePrompt(commands.image)">
          <div name="image" class="image_button">
            <font-awesome-icon class="image-icon" icon="image" />사진삽입
          </div>
        </button>
        <p class="red-explain">이미지 URL을 입력해 주세요.</p>
      </div>
    </editor-menu-bar>

    <div class="editor-container">
      <editor-content class="editor__content" :editor="editor" />
    </div>
  </div>
</template>

<script>
import { Editor, EditorContent, EditorMenuBar } from "tiptap";
import { Image } from "tiptap-extensions";
export default {
  name: "html-editer",
  components: {
    EditorContent,
    EditorMenuBar,
  },
  data() {
    return {
      editor: new Editor({
        extensions: [new Image()],
        content: ``,
        onUpdate: ({ getHTML }) => {
          this.html = getHTML();
        },
      }),
      html: "",
    };
  },
  methods: {
    showImagePrompt: function (command) {
      const src = prompt("Enter the url of your image here");
      if (src !== null) {
        command({ src });
      }
    },
    upload_html: function () {
      this.$emit("html", this.html);
    },
  },
  watch: { html: "upload_html" },
};
</script>

<style lang="scss" scoped>
.editor {
  .editor__content {
    height: 100%;
  }

  input,
  button {
    &:focus {
      outline: none;
    }
  }

  .image_button {
    display: inline-block;
    font-size: 13px;
    border: 1px solid #dddddd;
    border-radius: 5px;
    margin-right: 10px;
    padding: 6px 12px;
    background-color: white;
  }

  .manubar {
    display: flex;
    align-items: center;
  }
  .editor-container {
    width: 100%;
    height: 388px;
    border: 1px solid #dddddd;
    border-radius: 5px;
    margin-top: 10px;
    background-color: white;
  }
}
</style>
