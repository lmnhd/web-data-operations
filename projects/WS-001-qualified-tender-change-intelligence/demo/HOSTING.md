# Vercel adapter

The user approved Vercel on the existing account, rather than a new Render service. This preserves the real Python engine while making the transport stateless.

## Implementation

- `app.py` is the Flask/Vercel entrypoint. Its fixed routes call `demo_server.run_case`, which calls the unchanged `tender_pipeline.run_pipeline`.
- Each successful run returns the complete JSON report and CSV text. The browser downloads that response directly; it does not rely on a particular warm server instance or a shared in-memory cache.
- Only the allowlisted saved public records and synthetic fixture are available. No user uploads, credentials, external data collection or persistence are required.
- The hosted check button executes 14 fixed core tests in-process. It does not execute arbitrary commands or launch subprocesses. The full local/CI suite contains 22 tests, including HTTP and hosted-adapter checks.
- JSON request size is capped at 8 KB; cross-site browser POSTs are rejected; script/style sources are restricted; the function has a 15-second duration cap. A per-instance 10-second check cooldown is a convenience guard, not a global rate limit.
- Public usage can consume Vercel account quota. No claim is made that an existing subscription guarantees zero incremental usage cost. Do not enable paid add-ons or raise account spending limits without approval.

## Run locally

From this project directory:

```powershell
python -m pip install -r requirements.txt
python -m flask --app app run --port 8766
```

The original stdlib server remains available for the original local workflow. Its server-side export endpoints still work; the shared browser now downloads the returned result without a second server request.

## Deployment

Deploy this project directory, not the full archive or the Source root. The `.vercelignore` excludes screenshot collections and saved run outputs. Sanitized capture JSON, core tests and fixtures must remain bundled because they are the demonstration inputs.

Vercel CLI login needs user authorization. Verify the correct existing team and plan before deployment. Do not expose a personal machine through a tunnel. A hosted URL is not a completed Upwork publication: verify the uploaded PDF and portfolio entry separately.

Official reference: https://vercel.com/docs/functions/runtimes/python
