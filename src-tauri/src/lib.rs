mod runner;

use runner::{RunRequest, RunResponse, ToolchainPrefs, ToolchainStatus};
use tauri::{Emitter, Manager};

#[tauri::command]
async fn run_code(req: RunRequest) -> RunResponse {
    runner::run_code(req).await
}

#[tauri::command]
async fn check_toolchain(prefs: Option<ToolchainPrefs>) -> ToolchainStatus {
    runner::check_toolchain(prefs.unwrap_or_default()).await
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let mut builder = tauri::Builder::default();

    // Desktop: a second launch (e.g. the OS opening logicquest://auth-callback)
    // forwards its URL to the running window instead of opening a new one.
    #[cfg(desktop)]
    {
        builder = builder.plugin(tauri_plugin_single_instance::init(|app, argv, _cwd| {
            if let Some(url) = argv.iter().find(|a| a.starts_with("logicquest://")) {
                let _ = app.emit("deep-link-url", url.clone());
            }
            if let Some(w) = app.get_webview_window("main") {
                let _ = w.unminimize();
                let _ = w.set_focus();
            }
        }));
    }

    builder
        .plugin(tauri_plugin_deep_link::init())
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            // Windows/Linux need the URL scheme registered at runtime (dev builds and AppImage).
            #[cfg(any(windows, target_os = "linux"))]
            {
                use tauri_plugin_deep_link::DeepLinkExt;
                let _ = app.deep_link().register_all();
            }
            let _ = app;
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![run_code, check_toolchain])
        .run(tauri::generate_context!())
        .expect("error while running LogicQuest");
}
