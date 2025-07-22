document.addEventListener("DOMContentLoaded", function () {
  // Global div oluştur
  const globalKeyboardDiv = document.createElement("div");
  globalKeyboardDiv.className = "simple-keyboard custom-keyboard";
  globalKeyboardDiv.style.display = "none";
  globalKeyboardDiv.style.position = "absolute";
  globalKeyboardDiv.style.zIndex = "9999";
  document.body.appendChild(globalKeyboardDiv);

  // Önizleme barı (sadece number için)
  const previewBar = document.createElement("div");
  previewBar.className = "keyboard-preview";
  previewBar.style.display = "none";
  previewBar.style.position = "absolute";
  previewBar.style.background = "#3D74FF";
  previewBar.style.color = "#FFF";
  previewBar.style.fontFamily = "Arial, sans-serif";
  previewBar.style.fontSize = "28px";
  previewBar.style.fontWeight = "bold";
  previewBar.style.padding = "22px 4px";
  previewBar.style.borderRadius = "22px";
  previewBar.style.pointerEvents = "none";
  previewBar.style.zIndex = "10000";
  document.body.appendChild(previewBar);

  let keyboard;
  let activeInput = null;
  let bufferValue = "";
  let currentLayout = "default";
  let isNumberMode = false;

  // Türkçe Q layout
  const turkishLayout = {
    default: [
      "1 2 3 4 5 6 7 8 9 0 - _ {bksp}",
      "q w e r t y u ı o p ğ ü",
      "a s d f g h j k l ş i , {enter}",
      "{shift} z x c v b n m ö ç .",
      "{tab} {space}"
    ],
    shift: [
      "! \" ^ + % & / ( ) = ? * {bksp}",
      "Q W E R T Y U I O P Ğ Ü",
      "A S D F G H J K L Ş İ ; {enter}",
      "{shift} Z X C V B N M Ö Ç :",
      "{tab} {space}"
    ]
  };

  // Numerik layout (virgül ve nokta destekli)
  const numericLayout = {
    default: [
      "1 2 3",
      "4 5 6",
      "7 8 9",
      "0 . {bksp} {enter}"
    ]
  };

  // Klavyeyi oluştur
  keyboard = new window.SimpleKeyboard.default({
    onChange: (input) => {
      if (!activeInput) return;

      if (isNumberMode) {
        // Number input: buffer'a yaz
        bufferValue = input;
        // önizlemeyi güncelle
        previewBar.textContent = bufferValue || "(boş)";
      } else {
        // Text veya diğerleri: direkt input'a yaz
        activeInput.value = input;
        requestAnimationFrame(() => {
          activeInput.focus();
          activeInput.setSelectionRange(input.length, input.length);
        });
        activeInput.dispatchEvent(new Event("input", { bubbles: true }));
      }
    },
    onKeyPress: (button) => {
      if (button === "{shift}") {
        currentLayout = currentLayout === "default" ? "shift" : "default";
        keyboard.setOptions({ layoutName: currentLayout });
        document.querySelectorAll(".hg-button-shift").forEach(btn => {
          btn.classList.toggle("active", currentLayout === "shift");
        });
      }
      if (button === "{enter}") {
        // Number moddaysa buffer'ı input'a kaydet
        if (isNumberMode && activeInput) {
          activeInput.value = bufferValue;
          activeInput.dispatchEvent(new Event("input", { bubbles: true }));
        }
        closeKeyboard();
      }
    },
    rootElement: globalKeyboardDiv,
    theme: "hg-theme-default hg-layout-default custom-theme",
    display: {
      "{bksp}": "Sil",
      "{enter}": "Enter",
      "{shift}": "Shift",
      "{tab}": "Tab",
      "{space}": "Boşluk"
    }
  });

  // Klavyeyi aç
function openKeyboard(input) {
  activeInput = input;
  isNumberMode = input.type === "number";

    if (isNumberMode) {
      bufferValue = input.value || "";
      keyboard.setOptions({ layout: numericLayout, layoutName: "default" });
      globalKeyboardDiv.classList.add("number-mode");
      previewBar.classList.add("with-caret");   // caret aç
    } else {
      keyboard.setOptions({ layout: turkishLayout, layoutName: currentLayout });
      globalKeyboardDiv.classList.remove("number-mode");
      previewBar.classList.remove("with-caret"); // caret kapat
    }

  const rect = input.getBoundingClientRect();
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

  // 👉 Number moddaysa daha küçük genişlik kullan
  const desiredWidth = isNumberMode ? 300 : 1000;  // istediğin boyutu buradan değiştir
  const maxWidth = window.innerWidth - 40;

  let left = rect.left + scrollLeft;
  if (left + desiredWidth > window.innerWidth) {
    left = window.innerWidth - desiredWidth - 20;
    if (left < 0) left = 0;
  }

  globalKeyboardDiv.style.top = rect.bottom + scrollTop + 8 + "px";
  globalKeyboardDiv.style.left = left + "px";
  globalKeyboardDiv.style.width = Math.min(desiredWidth, maxWidth) + "px";
  globalKeyboardDiv.style.display = "block";

  if (isNumberMode) {
    previewBar.style.top = rect.top + scrollTop - 40 + "px";
    previewBar.style.left = left + "px";
    previewBar.textContent = bufferValue || "(boş)";
    previewBar.style.display = "block";
    keyboard.setInput(bufferValue);
  } else {
    previewBar.style.display = "none";
    keyboard.setInput(input.value);
  }
}


  // Klavyeyi kapat
function closeKeyboard() {
  globalKeyboardDiv.style.display = "none";
  previewBar.style.display = "none";
  previewBar.classList.remove("with-caret");  // caret’i de kaldır
  
    // 👇 Burada ekle: aktif inputtan big-input sınıfını kaldır
  if (activeInput) {
    activeInput.classList.remove('big-input');
  }
  
  activeInput = null;
  isNumberMode = false;
}

  // Focus olunca aç (ama sayi classı varsa açma!)
  document.addEventListener("focusin", (e) => {
    const input = e.target;

    // Sadece input veya textarea
    const isValid =
      (input.tagName === "INPUT" &&
        !["button", "submit", "checkbox", "radio", "file", "reset", "hidden"].includes(input.type)) ||
      input.tagName === "TEXTAREA";

    if (!isValid) return;

    // Eğer sayi classı varsa klavye açma
    if (input.classList.contains("form-control-sayi")) {
      return;
    }

    openKeyboard(input);
  });

  // Dışına tıklayınca kapat
  document.addEventListener("mousedown", (e) => {
    if (
      !e.target.closest("input") &&
      !e.target.closest("textarea") &&
      !e.target.closest(".simple-keyboard")
    ) {
      closeKeyboard();
    }
  });

  // Resize olunca kapat
  window.addEventListener("resize", closeKeyboard);
});

document.querySelectorAll('input[type="text"], input[type="number"], input[type="email"]').forEach(inp => {
  inp.addEventListener('focus', function() {
    this.classList.add('big-input');
  });
});
