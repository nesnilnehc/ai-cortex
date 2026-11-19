# Doubao narration

- If the user selects Doubao Speech 2.0 Dayi 2.0, verify that the selected account supports resource `seed-tts-2.0` and voice `zh_male_dayi_uranus_bigtts`. Reuse pacing and style settings already validated for the video, or verify them with a short sample. Read credentials through hidden terminal input or a configured secure credential source.
- Prefer asynchronous long-text synthesis for a full script and request word timings when supported. Check the current limits, billing, required markers, and voice parameters before submission. Save the task ID and query the same task to recover a result or refresh a download URL. Preserve any required audio cue as the service permits and avoid repeating it at each slide boundary.
- If the interface supports Speech Synthesis Markup Language (SSML), use phonetic markup to test a short sample for difficult terms. Check the returned audio, timestamps, and billing receipt separately. SSML results may omit word timings, and markup may count toward billable characters. Use the local alignment options in [Production and verification](production.md#timing-and-pronunciation-repair) when needed.

## Provider documentation

- [Submit a long-text synthesis task](https://docs.volcengine.com/docs/doubao-voice/task-sub-mission?lang=zh)
- [Query a synthesis task](https://docs.volcengine.com/docs/doubao-voice/result-query?lang=zh)
- [SSML reference](https://docs.volcengine.com/docs/doubao-voice/ssm-lmarkuplanguage?lang=zh)
- [Billing overview](https://docs.volcengine.com/docs/doubao-voice/billing-overview?lang=zh)
