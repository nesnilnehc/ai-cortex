export function bindCopyButton(button, source, feedback, clipboard, messages = {
  copying: 'Copying commands…',
  success: 'Commands copied. Paste them into your terminal.',
  unavailable: 'Copy unavailable. Select and copy the commands below.',
  empty: 'Commands unavailable. Open the installation guide below.',
}) {
  button.addEventListener('click', async () => {
    if (button.disabled) return;
    const commands = source.textContent.trim();
    if (!commands) {
      feedback.textContent = messages.empty;
      return;
    }
    button.disabled = true;
    feedback.textContent = messages.copying;
    try {
      await clipboard.writeText(commands);
      feedback.textContent = messages.success;
    } catch {
      feedback.textContent = messages.unavailable;
    } finally {
      button.disabled = false;
    }
  });
  button.hidden = false;
}
