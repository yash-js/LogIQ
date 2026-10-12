//! Local progress storage in SQLite, plus backups.
//!
//! The whole progress document is one JSON value under the key "progress".
//! A copy of the database is kept in `backups/` once per day (last 14 days).

use rusqlite::{params, Connection, OptionalExtension};
use serde::Serialize;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

pub struct Store {
    conn: Mutex<Connection>,
    pub dir: PathBuf,
}

const KEEP_BACKUPS: usize = 14;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct DataInfo {
    pub data_dir: String,
    pub db_path: String,
    pub backups: Vec<String>,
}

impl Store {
    pub fn open(dir: &Path) -> Result<Self, String> {
        std::fs::create_dir_all(dir).map_err(|e| e.to_string())?;
        let conn = Connection::open(dir.join("logicquest.db")).map_err(|e| e.to_string())?;
        conn.execute_batch(
            "PRAGMA journal_mode = WAL;
             CREATE TABLE IF NOT EXISTS kv (
               key        TEXT PRIMARY KEY,
               value      TEXT NOT NULL,
               updated_at TEXT NOT NULL DEFAULT (datetime('now'))
             );",
        )
        .map_err(|e| e.to_string())?;
        Ok(Self { conn: Mutex::new(conn), dir: dir.to_path_buf() })
    }

    pub fn get(&self, key: &str) -> Result<Option<String>, String> {
        let conn = self.conn.lock().map_err(|e| e.to_string())?;
        conn.query_row("SELECT value FROM kv WHERE key = ?1", params![key], |r| r.get(0))
            .optional()
            .map_err(|e| e.to_string())
    }

    pub fn set(&self, key: &str, value: &str) -> Result<(), String> {
        {
            let conn = self.conn.lock().map_err(|e| e.to_string())?;
            conn.execute(
                "INSERT INTO kv (key, value, updated_at) VALUES (?1, ?2, datetime('now'))
                 ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
                params![key, value],
            )
            .map_err(|e| e.to_string())?;
        }
        let _ = self.daily_backup();
        Ok(())
    }

    fn backup_dir(&self) -> PathBuf {
        self.dir.join("backups")
    }

    /// Copies the database to backups/progress-YYYY-MM-DD.db once a day.
    pub fn daily_backup(&self) -> Result<(), String> {
        let dir = self.backup_dir();
        std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
        let today: String = {
            let conn = self.conn.lock().map_err(|e| e.to_string())?;
            conn.query_row("SELECT date('now', 'localtime')", [], |r| r.get(0)).map_err(|e| e.to_string())?
        };
        let target = dir.join(format!("progress-{today}.db"));
        if target.exists() {
            return Ok(());
        }
        {
            let conn = self.conn.lock().map_err(|e| e.to_string())?;
            conn.execute("VACUUM INTO ?1", params![target.to_string_lossy()]).map_err(|e| e.to_string())?;
        }
        let mut files = self.list_backups();
        files.sort();
        while files.len() > KEEP_BACKUPS {
            let old = files.remove(0);
            let _ = std::fs::remove_file(dir.join(old));
        }
        Ok(())
    }

    pub fn list_backups(&self) -> Vec<String> {
        let mut v: Vec<String> = std::fs::read_dir(self.backup_dir())
            .map(|rd| {
                rd.filter_map(|e| e.ok())
                    .map(|e| e.file_name().to_string_lossy().to_string())
                    .filter(|n| n.starts_with("progress-") && n.ends_with(".db"))
                    .collect()
            })
            .unwrap_or_default();
        v.sort();
        v.reverse();
        v
    }

    /// Reads the progress JSON out of one of the daily backup databases.
    pub fn read_backup(&self, name: &str) -> Result<Option<String>, String> {
        if name.contains('/') || name.contains('\\') || name.contains("..") {
            return Err("Invalid backup name".into());
        }
        let conn = Connection::open(self.backup_dir().join(name)).map_err(|e| e.to_string())?;
        conn.query_row("SELECT value FROM kv WHERE key = 'progress'", [], |r| r.get(0))
            .optional()
            .map_err(|e| e.to_string())
    }

    pub fn info(&self) -> DataInfo {
        DataInfo {
            data_dir: self.dir.to_string_lossy().to_string(),
            db_path: self.dir.join("logicquest.db").to_string_lossy().to_string(),
            backups: self.list_backups(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roundtrip_and_backup() {
        let dir = std::env::temp_dir().join(format!("lq-store-test-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        let s = Store::open(&dir).unwrap();
        assert_eq!(s.get("progress").unwrap(), None);
        s.set("progress", r#"{"xp":10}"#).unwrap();
        s.set("progress", r#"{"xp":25}"#).unwrap();
        assert_eq!(s.get("progress").unwrap().as_deref(), Some(r#"{"xp":25}"#));
        let backups = s.list_backups();
        assert_eq!(backups.len(), 1, "one backup per day");
        // The day's backup holds the first save of that day.
        assert_eq!(s.read_backup(&backups[0]).unwrap().as_deref(), Some(r#"{"xp":10}"#));
        assert!(s.read_backup("../x.db").is_err());
        drop(s);
        let s2 = Store::open(&dir).unwrap();
        assert_eq!(s2.get("progress").unwrap().as_deref(), Some(r#"{"xp":25}"#));
        let _ = std::fs::remove_dir_all(&dir);
    }
}
