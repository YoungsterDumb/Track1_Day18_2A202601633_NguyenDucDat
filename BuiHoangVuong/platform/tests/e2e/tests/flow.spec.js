import { expect, test } from "@playwright/test";

async function signIn(page) {
  await page.goto("/");
  await page.getByLabel("Tài khoản").fill("teacher");
  await page.getByLabel("Mật khẩu").fill("teacher123");
  await page.getByRole("button", { name: "Đăng nhập" }).click();
  await expect(page.getByRole("button", { name: "In-Class" })).toBeVisible();
}

test("rejects wrong credentials", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Tài khoản").fill("teacher");
  await page.getByLabel("Mật khẩu").fill("wrong-password");
  await page.getByRole("button", { name: "Đăng nhập" }).click();
  await expect(page.getByRole("alert")).toContainText("Invalid username or password");
});

test("in-class: sync, score, rank, and explain", async ({ page }) => {
  await signIn(page);
  await page.getByRole("button", { name: "🔄 Sync School Data" }).click();
  await expect(page.locator(".status")).toContainText("Đã đồng bộ 50 học sinh");

  await page.getByRole("button", { name: "⚡ Calculate Risk Scores" }).click();
  await expect(page.locator(".status")).toContainText("Chấm điểm xong: 50 học sinh", { timeout: 30_000 });

  const rows = page.locator('[data-testid="ranking-table"] tbody tr');
  await expect(rows).toHaveCount(50);
  await expect(rows.first().locator(".pill")).toHaveText("75");

  await rows.first().getByRole("button", { name: "Why?" }).click();
  await expect(page.getByTestId("explanation")).toContainText("Xếp hạng #1 với 75/100 điểm rủi ro");
});

test("in-class: category filter narrows the table", async ({ page }) => {
  await signIn(page);
  await page.selectOption("select", "High Risk");
  const pills = page.locator('[data-testid="ranking-table"] tbody .pill.high');
  await expect(pills.first()).toBeVisible();
  await expect(page.locator('[data-testid="ranking-table"] tbody .pill.low')).toHaveCount(0);
});

test("course-long: analytics, progress, and intervention lifecycle", async ({ page }) => {
  await signIn(page);
  await page.getByRole("button", { name: "Course-Long" }).click();

  await expect(page.getByTestId("analytics")).toContainText("Học sinh");
  await expect(page.locator('[data-testid="progress-table"] tbody tr')).toHaveCount(20);

  await page.getByPlaceholder("Student ID").fill("1");
  await page.getByPlaceholder("Ghi chú").fill("E2E: đặt lịch phụ đạo");
  await page.getByRole("button", { name: "+ Tạo can thiệp" }).click();

  const firstRow = page.locator('[data-testid="interventions-table"] tbody tr').first();
  await expect(firstRow.locator(".pill")).toHaveText("open");
  await firstRow.getByRole("button", { name: "Đóng" }).click();
  await expect(page.locator('[data-testid="interventions-table"] tbody tr').first().locator(".pill")).toHaveText("resolved");
});

test("session survives a reload and clears on sign out", async ({ page }) => {
  await signIn(page);
  await page.reload();
  await expect(page.getByRole("button", { name: "In-Class" })).toBeVisible();
  await page.getByRole("button", { name: "Đăng xuất" }).click();
  await expect(page.getByRole("button", { name: "Đăng nhập" })).toBeVisible();
});
