# EventHub Deployment Checklist

## Pre-Deployment

- [x] Fixed dashboard route with eager loading
- [x] Added comprehensive error handling
- [x] Updated SQLAlchemy version for compatibility
- [x] Added production logging
- [x] Added global error handlers (500, 404)
- [x] Added health check endpoint
- [x] Verified Python syntax (no compilation errors)

## Deploy to Render

### Step 1: Commit Changes
```bash
git add app.py requirements.txt TROUBLESHOOTING.md DEPLOYMENT_CHECKLIST.md
git commit -m "Fix: Dashboard 500 error - Add eager loading, error handling, and logging"
git push origin main
```

### Step 2: Monitor Render Deployment
1. Go to https://dashboard.render.com
2. Select your `eventhub` service
3. Watch the deployment logs for:
   - ✅ Dependencies installation
   - ✅ Database migrations (`flask db upgrade`)
   - ✅ Admin user creation
   - ✅ Service start with gunicorn

### Step 3: Verify Deployment
```bash
# Test health endpoint
curl https://eventhub-s1xx.onrender.com/health

# Expected response:
# {"status":"healthy","database":"connected","timestamp":"2026-04-26T..."}
```

### Step 4: Test Dashboard
1. Navigate to https://eventhub-s1xx.onrender.com
2. Login as organizer (use credentials from `create_admin_users.py`)
3. Click "Dashboard" or go to `/dashboard`
4. Verify all sections load:
   - Events table
   - Venues table
   - Speakers table
   - Recent Orders table
   - Statistics cards

## Post-Deployment Verification

### Check Logs
```bash
# In Render Dashboard:
# Service → Logs → Filter by "error" or "Dashboard"
```

### Test All Dashboard Features
- [ ] View events list
- [ ] View venues list
- [ ] View speakers list
- [ ] View orders list
- [ ] Statistics cards display correctly
- [ ] Create new event button works
- [ ] Edit/Delete buttons work

### Performance Check
- [ ] Dashboard loads in < 3 seconds
- [ ] No N+1 query warnings in logs
- [ ] Memory usage is stable

## Rollback Plan (If Needed)

If the deployment fails:

```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Or rollback in Render dashboard:
# Service → Settings → Manual Deploy → Select previous deployment
```

## Environment Variables to Verify

In Render dashboard, check these are set:
- `FLASK_APP=app.py`
- `FLASK_ENV=production`
- `SECRET_KEY` (auto-generated)
- `PYTHON_VERSION=3.11.0`

## Database Verification

If dashboard still fails, check database:

```bash
# In Render Shell (if available)
python
>>> from app import app, db, Order, User, Event
>>> with app.app_context():
...     print(f"Users: {User.query.count()}")
...     print(f"Events: {Event.query.count()}")
...     print(f"Orders: {Order.query.count()}")
```

## Success Criteria

✅ Health endpoint returns 200 OK
✅ Dashboard loads without 500 error
✅ All tables display data (or empty state)
✅ No errors in Render logs
✅ Can create/edit/delete events
✅ Statistics cards show correct counts

## Next Steps After Successful Deployment

1. Monitor error logs for 24 hours
2. Check performance metrics
3. Test all organizer features
4. Test attendee ticket booking flow
5. Verify QR code generation works
6. Test reminder system

## Support

If issues persist after deployment:
1. Check TROUBLESHOOTING.md
2. Review Render logs
3. Test health endpoint
4. Verify database connectivity
5. Check disk mount status in render.yaml
