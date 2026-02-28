# Custom OpenClaw with Pillow pre-installed
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Install Pillow and other common packages
RUN pip install Pillow --user

# Optional: Install other useful packages
# RUN pip install requests beautifulsoup4 lxml --user

USER node

# Keep existing entrypoint
ENTRYPOINT ["openclaw"]
