# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

### Application Nature
AutoKeyboard is a **keyboard automation tool** that by nature:
- **Captures keyboard input** when recording is active
- **Simulates keyboard input** during playback
- **Operates at system level** for global hotkey functionality

### What We Do to Protect Users

#### Data Privacy
- ✅ **No network access** - Application never connects to the internet
- ✅ **Local storage only** - All data stays on your computer
- ✅ **No telemetry** - No usage data is collected or transmitted
- ✅ **No logging of sensitive keys** - Recording can be controlled by the user

#### Safe Operation
- ✅ **User control** - Recording only happens when explicitly started
- ✅ **Clear indicators** - UI clearly shows when recording is active
- ✅ **Hotkey filtering** - Application hotkeys are not recorded
- ✅ **Open source** - All code is available for inspection

#### File Security
- ✅ **Local configuration** - Settings stored in user profile directory
- ✅ **No elevated privileges** - Runs with standard user permissions
- ✅ **Sandboxed operation** - Cannot access files outside user permissions

### Potential Security Implications

#### False Positives
- **Antivirus warnings** are common due to keyboard simulation capabilities
- **Not signed** with expensive code signing certificates
- **Compiled Python** executables are often flagged by heuristic detection

#### Legitimate Concerns
- Could be **misused for malicious purposes** if distributed deceptively
- **Workplace policies** may prohibit automation tools
- **Game anti-cheat** systems may flag automation software

### What Users Should Know

#### Before Using
1. **Verify source** - Only download from official repository
2. **Check file hashes** - Verify integrity of downloaded files
3. **Review permissions** - Understand what the application can access
4. **Workplace compliance** - Ensure automation is permitted in your environment

#### While Using
1. **Be mindful of recording** - Don't record sensitive information
2. **Secure your scripts** - Protect saved automation scripts
3. **Log off when away** - Don't leave automation running unattended
4. **Review automations** - Understand what your scripts will do

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **DO NOT** create a public issue
2. **Email** security concerns privately to: [maintainer email]
3. **Include** detailed information about the vulnerability
4. **Allow** reasonable time for response and fixes

### Response Process

When security issues are reported:

1. **Acknowledgment** within 48 hours
2. **Assessment** of severity and impact
3. **Fix development** in private repository
4. **Coordinated disclosure** after fix is ready
5. **Public advisory** with mitigation steps

### Best Practices for Users

#### Installation
- Download only from official sources
- Verify file integrity when possible
- Use antivirus software (expect false positives)
- Consider running from Python source for maximum transparency

#### Usage
- Don't automate sensitive operations
- Be cautious with scripts from others
- Regularly review saved automation scripts
- Use in compliance with applicable policies

#### Storage
- Keep automation scripts secure
- Don't share scripts containing sensitive sequences
- Regularly clean up old/unused automations
- Back up important scripts securely

### Disclaimer

AutoKeyboard is provided "as is" without warranty. Users are responsible for:
- Ensuring compliance with applicable laws and policies
- Protecting their systems and data
- Using the software ethically and responsibly
- Understanding the security implications of automation tools

The developers are not responsible for misuse of this software or any consequences arising from its use.

---

**Remember: This tool simulates user input and should be used responsibly and in compliance with all applicable laws and policies.**
