// Cek apakah tanggal adalah hari ini
export function isToday(dateString) {
  const today = new Date();
  const date = new Date(dateString);
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
}

// Cek apakah tanggal masih dalam X hari terakhir (default 7 hari)
export function isRecent(dateString, days = 7) {
  const now = new Date();
  const date = new Date(dateString);
  const diff = (now - date) / (1000 * 60 * 60 * 24);
  return diff <= days && diff >= 0;
}