mod runner;
mod store;

use runner::{RunRequest, RunResponse, ToolchainPrefs, ToolchainStatus};
use store::{DataInfo, Store};
use tauri::{Manager, State};

#[tauri::command]
async fn run_code(req: RunRequest) -> RunResponse {
    runner::run_code(req).await
}

#[tauri::command]
async fn check_toolchain(prefs: Option<ToolchainPrefs>) -> ToolchainStatus {
    runner::check_toolchain(prefs.unwrap_or_default()).await
}

#[tauri::command]
fn load_state(store: State<'_, Store>) -> Result<Option<String>, String> {
    store.get("progress")
}

#[tauri::command]
fn save_state(store: State<'_, Store>, value: String) -> Result<(), String> {
    store.set("progress", &value)
}

#[tauri::command]
fn data_info(store: State<'_, Store>) -> DataInfo {
    store.info()
}

#[tauri::command]
fn read_backup(store: State<'_, Store>, name: String) -> Result<Option<String>, String> {
    store.read_backup(&name)
}

/// Writes a backup file the learner picked with the save dialog.
#[tauri::command]
fn write_text_file(path: String, contents: String) -> Result<(), String> {
    std::fs::write(path, contents).map_err(|e| e.to_string())
}

/// Reads a backup file the learner picked with the open dialog.
#[tauri::command]
fn read_text_file(path: String) -> Result<String, String> {
    let meta = std::fs::metadata(&path).map_err(|e| e.to_string())?;
    if meta.len() > 50 * 1024 * 1024 {
        return Err("That file is too large to be a LogicQuest backup.".into());
    }
    std::fs::read_to_string(path).map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .setup(|app| {
            let dir = app.path().app_data_dir()?;
            let store = Store::open(&dir).map_err(|e| format!("Could not open the progress database in {}: {e}", dir.display()))?;
            app.manage(store);
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            run_code,
            check_toolchain,
            load_state,
            save_state,
            data_info,
            read_backup,
            write_text_file,
            read_text_file
        ])
        .run(tauri::generate_context!())
        .expect("error while running LogicQuest");
}
