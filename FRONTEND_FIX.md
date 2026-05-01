# 🔧 Frontend Fix & Troubleshooting Guide

## ✅ What I Fixed

### 1. **Duplicate JavaScript Functions** 
- Removed 8 duplicate function definitions in `static/script.js`
- Functions that were duplicated:
  - `addMessage()` - 2 versions
  - `newChat()` - 2 versions
  - `toggleSidebar()` - 2 versions
  - `createNewHistoryItem()` - 2 versions
  - Plus orphaned function code

### 2. **Missing CORS Configuration**
- Added `from flask_cors import CORS` in app.py
- Added `CORS(app)` initialization
- Allows frontend to make API calls

### 3. **Configuration Issues**
- Fixed duplicate `load_dotenv()` calls (was loading 3 times!)
- Removed debug `print()` statements
- Fixed config.py to use environment variables
- Properly set `app.secret_key`

### 4. **Database Connection**
- Updated `config.py` DevelopmentConfig to use `.env` DATABASE_URL
- Removed hardcoded empty password

---

## 🚀 How to Test Now

### **Step 1: Restart the App**

```bash
# Stop the running app (Ctrl+C)

# Clear Python cache
del /s /q __pycache__
del /s /q *.pyc

# Restart
python main.py
```

### **Step 2: Test in Browser**

Open **http://localhost:5000** and test these:

#### **A. Check Console for Errors**
1. Press **F12** to open Developer Tools
2. Click **Console** tab
3. Look for red error messages
4. Report any errors you see

#### **B. Test Chat (Without Login)**
1. Try typing a message in the chat box
2. Message should appear on the right side
3. Should see a "Typing..." indicator
4. Should get a response from the bot

#### **C. Test Login**
1. Click **Login** button in top-right
2. Go to **Login** page
3. Enter: `admin@university.com` / `admin123`
4. Click **Login**
5. Should redirect to admin dashboard

#### **D. Check Network Errors**
1. Open **F12 → Network** tab
2. Send a chat message
3. Look for `/chat` request
4. Should show **200 OK** status
5. Response should have `reply`, `type`, `intent`, `source`

---

## 🐛 If Still Having Issues

### **Issue: Chat doesn't send**
```
→ Check F12 Console for JavaScript errors
→ Check F12 Network tab - is /chat returning 200?
→ Ensure backend is running (you see Flask output)
```

### **Issue: API returns 500 error**
```
→ Check Flask console for errors
→ Try: python main.py init-db
→ Check MySQL is running
→ Check .env DATABASE_URL is correct
```

### **Issue: Login doesn't work**
```
→ Check F12 Console for errors
→ Try: mysql -u root -p (verify MySQL works)
→ Try: python main.py init-db (recreate database)
→ Check email is admin@university.com
```

### **Issue: Dashboard not loading**
```
→ Login might have failed
→ Check F12 Console for errors
→ Check /api/admin/exam-routines returns data
```

---

## 📋 Testing Checklist

After fixing, test these:

- [ ] Page loads without console errors
- [ ] Chat input field works
- [ ] Can type and send message
- [ ] Bot responds to messages
- [ ] Login button works
- [ ] Can login with admin credentials
- [ ] Admin dashboard loads
- [ ] User menu shows username
- [ ] Logout button works
- [ ] Can navigate back to chatbot

---

## 🔍 Browser Console Testing

If you want to manually test, open **F12 Console** and run:

```javascript
// Test 1: Check if frontend can talk to backend
fetch('/api/user/profile')
    .then(r => r.json())
    .then(d => console.log('Profile:', d))
    .catch(e => console.log('Error:', e))

// Test 2: Send a chat message
fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello' })
})
    .then(r => r.json())
    .then(d => console.log('Response:', d))
    .catch(e => console.log('Error:', e))

// Test 3: Check if page is responsive
document.getElementById('user-input').value = 'test message'
console.log('Input set successfully')
```

---

## 📊 Current File Status

| Component | Status | Notes |
|-----------|--------|-------|
| app.py | ✅ Fixed | CORS enabled, config fixed |
| script.js | ✅ Fixed | Removed duplicates |
| config.py | ✅ Fixed | Uses env variables |
| index.html | ✅ OK | No changes needed |
| login.html | ✅ OK | No changes needed |
| admin_routes.py | ✅ OK | No changes needed |
| teacher_routes.py | ✅ OK | No changes needed |

---

## 🎯 Next Steps

1. **Restart the app** with the fixes
2. **Test in browser** - follow the testing checklist above
3. **Check console** - F12 to see any remaining errors
4. **Share any errors** - if you still see issues, show me the console errors

---

## 💡 Common Frontend Issues Resolved

✅ Duplicate JavaScript functions causing conflicts - **FIXED**
✅ CORS not configured blocking API calls - **FIXED**
✅ Config not using environment variables - **FIXED**
✅ Database URL configuration issues - **FIXED**
✅ Groq client initialization issues - **FIXED** (from previous session)

---

## 📞 If Issues Persist

Run this in PowerShell to collect diagnostics:

```bash
# 1. Check backend is responding
curl http://localhost:5000/

# 2. Check API endpoint
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"test\"}"

# 3. Check login endpoint
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"email\": \"admin@university.com\", \"password\": \"admin123\"}"

# If any of these fail, backend has issues
```

---

**Try the fixes and let me know what you see! 🚀**
