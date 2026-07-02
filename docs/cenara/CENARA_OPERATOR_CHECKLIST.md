# Cenara operator checklist

## Railway/private access

- Set `GX1_ACCESS_TOKEN` before exposing the app.
- Open the Railway URL and enter the private token.
- Confirm the private Cenara command center loads.
- Confirm the badges show Private/Secure, Powered by GXEON, and MoneyPrinterTurbo MIT attribution.

## Required variables and providers

- Configure an LLM provider if the operator expects Cenara to generate scripts from a subject.
- Configure at least one video source:
  - Pexels key for Pexels.
  - Pixabay key for Pixabay.
  - Coverr key for Coverr.
  - Or use local uploaded media in the advanced MoneyPrinterTurbo controls.
- Configure a TTS voice/provider or use the supported custom/no-voice workflow.
- Confirm FFmpeg is available in the runtime.
- ImageMagick improves subtitle rendering and appears as optional when not detected.

## Browser test

1. Open the Railway URL.
2. Enter `GX1_ACCESS_TOKEN`.
3. Confirm **Central de Provedores** appears.
4. Fill **Tema do vídeo** with `video de teste para anúncio de café artesanal`.
5. Select Pexels if a Pexels key exists, otherwise select a configured source.
6. Select or enter an available voice.
7. Click **Gerar vídeo real**.
8. Confirm no error says subject/script are both empty.
9. Confirm a real `task_id` appears.
10. Wait for the backend render.
11. Confirm preview appears only when a real MP4 exists.
12. Download the MP4 and verify the downloaded file matches the previewed file.
13. Confirm the video appears in **Biblioteca**.

## MP4 validation

- The generated file must be a non-empty `.mp4` in the standard storage/task output area.
- The UI must show file size and generation date/time.
- The UI must not show a success message if no MP4 is found.
- The UI must not display API keys, secret tokens, or absolute internal paths.
