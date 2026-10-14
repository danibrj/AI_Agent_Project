(() => {
  "use strict";

  const config = window.CHAT_CONFIG || {};
  const apiBaseUrl = typeof config.apiBaseUrl === "string"
    ? config.apiBaseUrl.replace(/\/+$/, "")
    : "";

  const form = document.querySelector("#message-form");
  const input = document.querySelector("#message-input");
  const sendButton = document.querySelector("#send-button");
  const newConversationButton = document.querySelector("#new-conversation");
  const messageArea = document.querySelector("#message-area");
  const emptyState = document.querySelector("#empty-state");
  const conversationList = document.querySelector("#conversation-list");
  const historyEmpty = document.querySelector("#history-empty");
  const historyCount = document.querySelector("#history-count");
  const loadingIndicator = document.querySelector("#loading-indicator");
  const feedback = document.querySelector("#feedback");
  const notice = document.querySelector("#notice");

  let conversationId = null;
  let isSubmitting = false;
  let isLoadingConversation = false;

  function setFeedback(message) {
    feedback.textContent = message;
    feedback.hidden = !message;
  }

  function setNotice(message) {
    notice.textContent = message;
    notice.hidden = !message;
  }

  function updateControls() {
    const hasMessage = input.value.trim().length > 0;
    sendButton.disabled = isSubmitting || !hasMessage;
    input.disabled = isSubmitting;
    newConversationButton.disabled = isSubmitting;
    loadingIndicator.hidden = !isSubmitting;
    loadingIndicator.lastElementChild.textContent = isLoadingConversation
      ? "گفتگو در حال بارگذاری است..."
      : "دستیار در حال آماده‌کردن پاسخ است...";
    conversationList.querySelectorAll("button").forEach((button) => {
      button.disabled = isSubmitting;
    });
  }

  function scrollToLatest() {
    messageArea.scrollTo({
      top: messageArea.scrollHeight,
      behavior: "smooth"
    });
  }

  function addMessage(role, content) {
    emptyState.hidden = true;

    const message = document.createElement("article");
    message.className = `message message-${role}`;

    const avatar = document.createElement("span");
    avatar.className = "message-avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = role === "user" ? "شما" : "AI";

    const contentContainer = document.createElement("div");
    contentContainer.className = "message-content";

    const label = document.createElement("span");
    label.className = "message-label";
    label.textContent = role === "user" ? "شما" : "دستیار هوشمند";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.setAttribute("dir", "auto");
    bubble.textContent = content;

    contentContainer.append(label, bubble);
    message.append(avatar, contentContainer);
    messageArea.append(message);
    scrollToLatest();
  }

  async function requestJson(path, options = {}) {
    let response;
    try {
      response = await fetch(`${apiBaseUrl}${path}`, {
        method: options.method || "GET",
        headers: options.payload === undefined
          ? {}
          : { "Content-Type": "application/json" },
        body: options.payload === undefined
          ? undefined
          : JSON.stringify(options.payload)
      });
    } catch (error) {
      throw new Error(`ارتباط با سرور برقرار نشد. ${error.message}`);
    }

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error(
        response.ok
          ? "پاسخ سرور در قالب JSON معتبر نیست."
          : `سرور با خطای HTTP ${response.status} پاسخ داد.`
      );
    }

    if (!response.ok) {
      const detail = data && typeof data.detail === "string"
        ? data.detail
        : data && typeof data.message === "string"
          ? data.message
          : "";
      throw new Error(detail || `سرور با خطای HTTP ${response.status} پاسخ داد.`);
    }

    if (data === null || typeof data !== "object") {
      throw new Error("ساختار پاسخ سرور معتبر نیست.");
    }

    return data;
  }

  async function createConversation() {
    const data = await requestJson("/chat/conversations", {
      method: "POST",
      payload: {}
    });
    if (!Number.isInteger(data.conversation_id) || data.conversation_id <= 0) {
      throw new Error("شناسهٔ گفتگو در پاسخ سرور معتبر نیست.");
    }
    conversationId = data.conversation_id;
  }

  function formatConversationDate(createdAt) {
    const parsedDate = new Date(createdAt.replace(" ", "T"));
    return Number.isNaN(parsedDate.getTime())
      ? createdAt
      : parsedDate.toLocaleDateString("fa-IR");
  }

  function renderConversationList(conversations) {
    conversationList.replaceChildren();
    historyCount.textContent = new Intl.NumberFormat("fa-IR").format(conversations.length);
    historyEmpty.hidden = conversations.length > 0;

    conversations.forEach((conversation) => {
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.className = "history-item";
      button.type = "button";
      button.dataset.conversationId = String(conversation.conversation_id);
      button.setAttribute(
        "aria-current",
        conversation.conversation_id === conversationId ? "true" : "false"
      );

      const title = document.createElement("span");
      title.className = "history-item-title";
      title.textContent = conversation.title;

      const date = document.createElement("span");
      date.className = "history-item-date";
      date.textContent = formatConversationDate(conversation.created_at);

      button.append(title, date);
      button.addEventListener("click", () => {
        void openConversation(conversation.conversation_id);
      });
      item.append(button);
      conversationList.append(item);
    });
  }

  async function refreshConversationList() {
    const conversations = await requestJson("/chat/conversations");
    if (!Array.isArray(conversations)) {
      throw new Error("ساختار تاریخچهٔ گفتگوها معتبر نیست.");
    }
    renderConversationList(conversations);
  }

  async function openConversation(id) {
    if (isSubmitting || id === conversationId) {
      return;
    }

    isSubmitting = true;
    isLoadingConversation = true;
    setFeedback("");
    setNotice("");
    updateControls();

    try {
      const data = await requestJson(`/chat/conversations/${id}`);
      if (!Array.isArray(data.messages)) {
        throw new Error("ساختار پیام‌های گفتگو معتبر نیست.");
      }

      conversationId = data.conversation_id;
      messageArea.replaceChildren(emptyState);
      emptyState.hidden = data.messages.length > 0;
      data.messages.forEach((message) => {
        if (typeof message.role !== "string" || typeof message.content !== "string") {
          throw new Error("ساختار یکی از پیام‌های گفتگو معتبر نیست.");
        }
        addMessage(message.role, message.content);
      });
      await refreshConversationList();
    } catch (error) {
      setFeedback(error.message || "بارگذاری گفتگو ناموفق بود. دوباره تلاش کنید.");
    } finally {
      isSubmitting = false;
      isLoadingConversation = false;
      updateControls();
      scrollToLatest();
    }
  }

  async function sendMessage(text) {
    if (isSubmitting || !text) {
      return;
    }

    isSubmitting = true;
    setFeedback("");
    setNotice("");
    addMessage("user", text);
    updateControls();

    try {
      if (conversationId === null) {
        await createConversation();
      }

      const data = await requestJson("/chat", {
        method: "POST",
        payload: {
          conversation_id: conversationId,
          text
        }
      });

      if (typeof data.response !== "string") {
        throw new Error("پاسخ دستیار در قالب مورد انتظار نیست.");
      }

      if (data.response.startsWith("ERROR:")) {
        setFeedback(`خطای دستیار: ${data.response.slice("ERROR:".length).trim()}`);
      } else {
        addMessage("assistant", data.response);
      }

      input.value = "";
      resizeInput();
      await refreshConversationList();
    } catch (error) {
      setFeedback(error.message || "ارسال پیام ناموفق بود. دوباره تلاش کنید.");
    } finally {
      isSubmitting = false;
      updateControls();
      scrollToLatest();
      if (!input.disabled) {
        input.focus();
      }
    }
  }

  function resizeInput() {
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    void sendMessage(input.value.trim());
  });

  input.addEventListener("input", () => {
    resizeInput();
    updateControls();
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      form.requestSubmit();
    }
  });

  newConversationButton.addEventListener("click", () => {
    conversationId = null;
    messageArea.replaceChildren(emptyState);
    emptyState.hidden = false;
    conversationList.querySelectorAll(".history-item").forEach((button) => {
      button.setAttribute("aria-current", "false");
    });
    setFeedback("");
    setNotice("گفتگوی تازه آماده است. با ارسال پیام، گفتگوی جداگانه‌ای ساخته می‌شود.");
    input.value = "";
    resizeInput();
    updateControls();
    input.focus();
  });

  updateControls();
  void refreshConversationList().catch((error) => {
    setFeedback(error.message || "بارگذاری تاریخچهٔ گفتگوها ناموفق بود.");
  });
})();
