# How to Properly Restart After Database Changes

## 🔄 **Why Just Building Doesn't Work**

When you change the database seeder (adding new schools), **just building the project doesn't update the database**. The database only gets created/seeded on **first run** if it doesn't exist.

---

## ✅ **Proper Restart Process**

### **Option 1: Delete Database First (Recommended)**

#### **Step 1: Stop the App**
In Visual Studio, press **Shift+F5** or click the red stop button

#### **Step 2: Delete the Database**
In your project folder, delete these files:
- `mentalhealthdb.db`
- `mentalhealthdb.db-shm`
- `mentalhealthdb.db-wal`

**Quick way:** Open terminal and run:
```bash
del mentalhealthdb.db*
```

#### **Step 3: Restart the App**
Press **F5** in Visual Studio

The app will:
- ✅ Create a fresh database
- ✅ Seed it with all 31 schools
- ✅ Show updated data on the map

---

### **Option 2: Clean and Rebuild (More Thorough)**

#### **Step 1: Stop the App**
Press **Shift+F5**

#### **Step 2: Clean Solution**
In Visual Studio:
- Go to **Build** → **Clean Solution**
- Wait for it to complete

#### **Step 3: Delete Database**
```bash
del mentalhealthdb.db*
```

#### **Step 4: Rebuild**
- Go to **Build** → **Rebuild Solution**

#### **Step 5: Run**
Press **F5**

---

## 🚫 **What DOESN'T Work**

❌ **Just Building** - Keeps old database
```
Build → Build Solution  ❌ (Old data remains)
```

❌ **Hot Reload** - Doesn't trigger database changes
```
Save file and hope it updates  ❌ (Doesn't work for database)
```

---

## 🎯 **When You Need to Restart**

You need to delete the database and restart when you:

### **Database Schema Changes:**
- ✅ Added new schools
- ✅ Changed Resource properties
- ✅ Changed College properties
- ✅ Modified the seeder

### **Code-Only Changes (No Restart Needed):**
- ❌ Changed CSS styling
- ❌ Modified JavaScript
- ❌ Updated views (HTML)
- ❌ Changed controllers (sometimes hot reload works)

---

## 📋 **Quick Reference**

### **I added new schools:**
```bash
1. Stop app (Shift+F5)
2. del mentalhealthdb.db*
3. Start app (F5)
```

### **I changed CSS/JavaScript:**
```bash
1. Save file
2. Hard refresh browser (Ctrl+Shift+R or Ctrl+F5)
```

### **I changed a Controller:**
```bash
1. Stop app (Shift+F5)
2. Start app (F5)
```

---

## 🔍 **How to Verify Updates Worked**

After restarting, check:

1. **Console Output**
   Look for: `✓ Database seeded with XX colleges and their resources`
   
2. **Map Display**
   Count the markers - should match number of schools

3. **Stats Bar**
   Top of page shows college count

4. **Filter Buttons**
   Click each state filter to verify schools appear

5. **Check Database File**
   File `mentalhealthdb.db` should have a **new timestamp**

---

## 💡 **Pro Tips**

### **Batch File for Quick Reset**
Create `reset-database.bat`:
```batch
@echo off
echo Stopping app...
taskkill /F /IM MentalHealthDatabase.exe 2>nul
echo Deleting database...
del mentalhealthdb.db* 2>nul
echo Done! Now press F5 in Visual Studio
pause
```

### **Check Database Contents**
Want to see what's in the database?
1. Install **DB Browser for SQLite** (free)
2. Open `mentalhealthdb.db`
3. View the `Colleges` table

### **Automate It**
Add this to Program.cs to always recreate on startup (DEV ONLY):
```csharp
// Force database recreation (development only)
await context.Database.EnsureDeletedAsync();
await context.Database.EnsureCreatedAsync();
```

---

## 🎓 **Current Database Status**

After restarting with latest code:
- **31 Schools Total**
- **7 States:** Ohio, Kentucky, Indiana, Illinois, Michigan, Pennsylvania, New York
- **37+ Resources**
- **2 Ivy League Schools:** UPenn, Cornell
- **Students Covered:** 750,000+

---

## 🚀 **Ready to See the Updates?**

### **Right Now:**
1. **Make sure app is stopped** (Shift+F5)
2. **Delete database:** `del mentalhealthdb.db*`
3. **Start app:** Press F5
4. **Watch console** for seeding message
5. **Open browser** to see all 31 schools!

---

**Last Updated:** January 30, 2026 - Added Cornell University 🎓
