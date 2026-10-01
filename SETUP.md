# Publish

1. Create a public repository named SinthujanCoder under SinthujanCoder. Initialize with a README.
2. Upload README.md, assets/, scripts/ and .github/ from this package, preserving directories. Include the hidden .github folder.
3. The Update profile activity workflow runs on the first push and daily. It uses the repository GITHUB_TOKEN; no personal token is needed. If Actions is disabled, enable it and run the workflow manually.
4. Open https://github.com/SinthujanCoder.

The workflow only updates assets/activity.svg. A failed fetch leaves the previous graphic unchanged. Branch protection may require adjusting the workflow's update process. Contribution counts reflect what GitHub exposes to the workflow; private repository names and details are not requested or rendered.

Publishing has not yet occurred. The profile repository was not accessible through the connected plugin when this package was prepared. The plugin has no repository creation action.
