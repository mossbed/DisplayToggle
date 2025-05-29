# DisplayToggle

**DisplayToggle** is a lightweight Windows system tray application that allows users to switch display inputs on their monitors using DDC/CI commands — including `ddcalt` codes for monitors (like many LG models) that don’t respond to standard DDC inputs.  
The twist? **DisplayToggle is designed to work with [BetterDisplay](https://github.com/waydabber/BetterDisplay)**, a macOS utility by [waydabber](https://twitter.com/waydabber), and **requires BetterDisplay’s HTTP server to function**.

---

## ⚙️ What It Does

**DisplayToggle** sends HTTP requests to BetterDisplay’s built-in HTTP server, allowing Windows users to switch monitor inputs using DDC/CI — even when their displays require non-standard codes like `ddcalt`.  

If you use both a Mac and a Windows PC with shared monitors, **DisplayToggle** fills a critical void by making it simple to change inputs from the Windows side — with a simple click from the system tray.

---

## 🤝 Works With BetterDisplay (macOS)

This tool wouldn’t exist without [BetterDisplay](https://github.com/waydabber/BetterDisplay) — the only known tool that:

- ✅ Exposes alternate DDC codes (`ddcalt` values) for hard-to-control displays.
- ✅ Provides a local HTTP server that allows network-based input switching.

---

## 🔗 Required Setup

To use DisplayToggle, you must:

1. Be running **BetterDisplay Pro** on your Mac.
2. Enable the **HTTP server** feature in BetterDisplay.
3. Ensure your **Mac and Windows machines are on the same local network**.

> 🛑 Without BetterDisplay running with the HTTP server active, DisplayToggle will not work.

---

## 🚀 Why This Exists

We created DisplayToggle because there’s simply **nothing else like it for Windows**. After testing popular tools like:

- Monitorian  
- Twinkle Tray  
- ClickMonitorDDC  
- winddcutil  

…we found none of them worked reliably for monitors requiring `ddcalt` codes.

So we set out to build a clean, user-friendly Windows app that can talk to BetterDisplay over the network and toggle monitor inputs accordingly.

---

## 🛠️ How It Works

DisplayToggle reads from a `config.json` file that defines:

- Your monitors (identified by BetterDisplay’s `tagID`)
- Each monitor's available input types
- The specific `ddc` or `ddcalt` values to use

When you click a menu item from the system tray, DisplayToggle sends a request like:

``` http://your-mac-host.local:55777/set?tagID=3&ddcAlt=208&vcp=inputSelectAlt ```

If the request fails, **DisplayToggle logs the failed attempt in an `error_log.txt` file**.

---

## 🧾 Configuration Format (`config.json`)

This file tells DisplayToggle which displays you’re using and how to switch each one’s input using BetterDisplay’s HTTP server.

Below is a sample `config.json`:

    {
      "Display 1": {
        "HDMI 1": "http://your-mac.local:55777/set?tagID=1&ddcAlt=144&vcp=inputSelectAlt",
        "DisplayPort": "http://your-mac.local:55777/set?tagID=1&ddcAlt=145&vcp=inputSelectAlt"
      },
      "Display 2": {
        "HDMI 2": "http://your-mac.local:55777/set?tagID=2&ddcAlt=208&vcp=inputSelectAlt"
      }
    }

### 🔧 How to Customize:

- `"Display 1"` and `"Display 2"` are display *names* (you can name them whatever you like: `"Gaming Monitor"`, `"Work Display"`, etc.).
- `"HDMI 1"`, `"DisplayPort"` are the input *labels* that will appear in your tray menu.
- Each value is a full URL request to BetterDisplay’s HTTP server using:
  - `tagID` – the ID for your display (find this in BetterDisplay)
  - `vcp=inputSelect` or `vcp=inputSelectAlt` – depending on whether your monitor uses standard or alternate DDC
  - `ddcAlt=XXX` – the input code to switch to (can be decimal or hex, e.g. `0xd1`)
- You must use BetterDisplay Pro with the HTTP server enabled for these links to work.
- Your Windows and Mac devices must be on the same local network.

📝 Tip: If you're not sure which `ddc` values your display needs, use BetterDisplay on your Mac to test and find the correct ones.

---

## 🧪 Current Limitations

### 🧩 System Tray Quirk (Windows Limitation)

Windows only displays the system tray on the **main display**. This means:

- If you toggle your **main display to another input first**, you’ll **lose access to the tray icon**.
- Always toggle **non-main displays first**, and the main one last.

### 🚧 What’s Coming Next

We plan to address this limitation in the next version with:

- ✅ Global keyboard shortcuts  
- ✅ An optional on-screen overlay menu for selecting inputs  
- ✅ An interactive first-run setup wizard  

---

## 🧰 Troubleshooting

### 🛠 Display Not Switching?

If you're trying to switch inputs and nothing happens (especially on your main display), try re-selecting the currently active input first (e.g., HDMI 1) to "wake" the HTTP server on your Mac. After doing this, try switching to your desired input again.

---

## 📌 Setup Instructions

1. Install [BetterDisplay Pro](https://github.com/waydabber/BetterDisplay) on your Mac.
2. Enable the **HTTP server** feature inside BetterDisplay.
3. Run **DisplayToggle** on your Windows machine.
4. Configure your `config.json` file to match your displays and input values.
5. Launch DisplayToggle and switch inputs from the system tray.

---

## 📚 DDC Value Lookup

**BetterDisplay** is the best tool to discover working `ddc` or `ddcalt` values for your monitor inputs.

In the future, we may:
- Integrate a DDC lookup utility into DisplayToggle
- Maintain a **community wiki** listing common monitor models and their compatible DDC input values

---

## 🙏 Acknowledgments

- Huge thanks to [waydabber](https://github.com/waydabber) for developing **BetterDisplay**, without which this project would not be possible.
- **DisplayToggle is designed specifically to complement BetterDisplay**, not replace it.

---

## 📦 License

**DisplayToggle** is open source and released under the [BSD 3-Clause License](LICENSE).

> This project is freely available for modification and redistribution.  
> If you include it in a paid product or derivative, we kindly ask that you retain attribution and consider contributing improvements back to the project.

