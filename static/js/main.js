// static/js/main.js
(function () {
  // 공유 아이콘(<a>) 선택
  const linkBtn = document.querySelector(".share-buttons a");
  if (!linkBtn) return;

  // 1) 복사할 고정 URL (요청한 "첫 링크")
  const SHARE_URL = "https://pause-test.onrender.com/";

  // 2) Clipboard 복사 유틸
  async function copy(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      }
    } catch (_) {}
    // 폴백(iOS/구형)
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  }

  // 3) 토스트 표시 유틸 (자동 사라짐)
  function showToast(message = "링크가 복사되었습니다!") {
    // 스타일이 한 번만 주입되도록
    if (!document.getElementById("toast-style")) {
      const style = document.createElement("style");
      style.id = "toast-style";
      style.textContent = `
        @keyframes toast-fade {
          0% { opacity: 0; transform: translate(-50%, 10px); }
          10% { opacity: 1; transform: translate(-50%, 0); }
          90% { opacity: 1; transform: translate(-50%, 0); }
          100% { opacity: 0; transform: translate(-50%, 10px); }
        }
        .toast {
          position: fixed;
          left: 50%;
          bottom: calc(24px + env(safe-area-inset-bottom));
          transform: translateX(-50%);
          background: rgba(63, 63, 63, 0.8);
          color: #fff;
          padding: 10px 16px;
          border-radius: 12px;
          font-size: 14px;
          z-index: 9999;
          animation: toast-fade 1.8s ease forwards;
          pointer-events: none;
          white-space: nowrap;
        }
      `;
      document.head.appendChild(style);
    }
    const el = document.createElement("div");
    el.className = "toast";
    el.textContent = message;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1900);
  }

  // 4) 클릭 이벤트: 링크 이동 막고 복사 + 토스트
  linkBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const ok = await copy(SHARE_URL);
    showToast(ok ? "링크가 복사되었습니다!" : "복사에 실패했어요");
  });
})();
