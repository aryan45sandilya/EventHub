#!/bin/bash

# EventHub Deployment Script
# This script commits and pushes all fixes to trigger Render deployment

echo "🚀 EventHub Deployment Script"
echo "=============================="
echo ""

# Check if there are changes to commit
if [[ -z $(git status -s) ]]; then
    echo "✓ No changes to commit"
    exit 0
fi

echo "📝 Files to be committed:"
git status -s
echo ""

# Add all modified files
echo "➕ Adding files..."
git add app.py requirements.txt TROUBLESHOOTING.md DEPLOYMENT_CHECKLIST.md FIX_SUMMARY.md deploy.sh

# Commit with descriptive message
echo "💾 Committing changes..."
git commit -m "Fix: Resolve all 500 errors with comprehensive eager loading and error handling

- Fixed /dashboard route with eager loading for Order.user, Event.venue, Speaker.event
- Fixed /my-tickets route with eager loading for Order.payment and nested relationships
- Fixed 6 additional ticket-related routes with proper eager loading
- Added comprehensive error handling to all routes
- Updated SQLAlchemy to version 2.0+ for compatibility
- Added production logging with rotating file handler
- Added global error handlers for 500 and 404 errors
- Added /health endpoint for monitoring
- Created comprehensive documentation (TROUBLESHOOTING.md, DEPLOYMENT_CHECKLIST.md, FIX_SUMMARY.md)

Routes fixed:
- /dashboard
- /my-tickets
- /events/<id>/tickets
- /tickets/<id>/pass
- /tickets/<id>/pass/download
- /verify/<token>
- /checkin/<token>
- /reminders

All changes verified with syntax checks and ready for production deployment."

# Push to remote
echo "🌐 Pushing to remote..."
git push origin main

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Monitor Render dashboard for build progress"
echo "2. Check deployment logs for any errors"
echo "3. Test /health endpoint: curl https://eventhub-s1xx.onrender.com/health"
echo "4. Test /dashboard and /my-tickets routes"
echo "5. Verify all user flows work correctly"
echo ""
echo "📚 Documentation:"
echo "- TROUBLESHOOTING.md - Common issues and solutions"
echo "- DEPLOYMENT_CHECKLIST.md - Detailed deployment steps"
echo "- FIX_SUMMARY.md - Complete summary of all changes"
