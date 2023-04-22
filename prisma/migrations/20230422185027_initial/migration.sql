-- CreateTable
CREATE TABLE "BotUser" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "username" TEXT,
    "full_name" TEXT NOT NULL,
    "joined_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "left_at" DATETIME
);

-- CreateTable
CREATE TABLE "BotChat" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "title" TEXT,
    "username" TEXT,
    "type" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "BotUser_id_key" ON "BotUser"("id");

-- CreateIndex
CREATE UNIQUE INDEX "BotChat_id_key" ON "BotChat"("id");
