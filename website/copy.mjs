export function bindCopyButton(button, source, feedback, clipboard) {
  button.addEventListener('click', async () => {
    if (button.disabled) return;
    const commands = source.textContent.trim();
    if (!commands) {
      feedback.textContent = 'Commands unavailable. Open the installation guide below.';
      return;
    }
    button.disabled = true;
    feedback.textContent = 'Copying commands…';
    try {
      await clipboard.writeText(commands);
      feedback.textContent = 'Commands copied. Paste them into your terminal.';
    } catch {
      feedback.textContent = 'Copy unavailable. Select and copy the commands below.';
    } finally {
      button.disabled = false;
    }
  });
  button.hidden = false;
}
