# AskBuddy - Testing Guide

This guide helps you test all features of the AskBuddy platform.

## Setup for Testing

1. Run the application with sample data:
   ```bash
   python run.py
   ```
   When prompted, type 'y' to add sample data.

2. Open browser: http://localhost:5000

## Test Scenarios

### 1. Authentication Testing

#### Test User Registration
- [ ] Navigate to Register page
- [ ] Fill in: Name, Email, Password
- [ ] Select Role: Student
- [ ] Click Register
- [ ] Verify redirect to login page
- [ ] Verify success message

#### Test Login
- [ ] Use credentials: john@student.com / password123
- [ ] Verify redirect to student dashboard
- [ ] Check navbar shows username and reputation
- [ ] Verify role-specific menu items appear

#### Test Logout
- [ ] Click on username dropdown
- [ ] Click Logout
- [ ] Verify redirect to home page
- [ ] Verify session cleared

### 2. Student Features Testing

#### Test Ask Question
- [ ] Login as student (john@student.com)
- [ ] Click "Ask New Question"
- [ ] Enter title: "How to calculate derivatives?"
- [ ] Watch for similar question suggestions
- [ ] Add description with details
- [ ] Select subject: Mathematics
- [ ] Add tags: calculus, derivatives
- [ ] Upload an image (optional)
- [ ] Submit question
- [ ] Verify question appears in dashboard

#### Test Browse Questions
- [ ] Click "Questions" in navbar
- [ ] Verify all questions display
- [ ] Test search: type "photosynthesis"
- [ ] Test filter by subject: Biology
- [ ] Test filter by status: Solved
- [ ] Click on a question to view details

#### Test Answer Question
- [ ] Open any unsolved question
- [ ] Scroll to "Your Answer" section
- [ ] Write a detailed answer
- [ ] Submit answer
- [ ] Verify answer appears
- [ ] Check reputation increased by +5 points

#### Test Voting System
- [ ] Find an answer (not your own)
- [ ] Click upvote button
- [ ] Verify vote count increases
- [ ] Click upvote again to remove vote
- [ ] Try downvote button
- [ ] Verify vote count changes

#### Test Mark Best Answer
- [ ] Open your own question
- [ ] Find a good answer
- [ ] Click "Mark as Best"
- [ ] Verify answer marked with green badge
- [ ] Verify question status changed to "solved"
- [ ] Check answer author got +15 reputation

#### Test Leaderboard
- [ ] Click "Leaderboard" in navbar
- [ ] Verify students ranked by reputation
- [ ] Check top 3 have trophy icons
- [ ] Click on a student name
- [ ] Verify profile page opens

#### Test Profile Page
- [ ] Click on your username
- [ ] Click "My Profile"
- [ ] Verify statistics display correctly
- [ ] Check Questions tab shows your questions
- [ ] Check Answers tab shows your answers
- [ ] Verify reputation points match

### 3. Teacher Features Testing

#### Test Teacher Login
- [ ] Logout current user
- [ ] Login as: robert@teacher.com / password123
- [ ] Verify teacher dashboard appears
- [ ] Check statistics display

#### Test Answer as Teacher
- [ ] Browse questions
- [ ] Open any question
- [ ] Submit an answer
- [ ] Verify "Teacher" badge appears on answer

#### Test Mark Correct Answer
- [ ] Open any question
- [ ] Click "Mark as Best" on any answer
- [ ] Verify question marked as solved
- [ ] Verify answer marked as best

#### Test Upload Study Material
- [ ] Click "Upload Study Material"
- [ ] Enter title: "Algebra Notes Chapter 1"
- [ ] Select subject: Mathematics
- [ ] Upload a PDF file
- [ ] Submit
- [ ] Verify success message

#### Test View Study Materials
- [ ] Click "Study Materials" in navbar
- [ ] Verify uploaded material appears
- [ ] Test filter by subject
- [ ] Click download button
- [ ] Verify file downloads

#### Test Content Moderation
- [ ] Open any question with answers
- [ ] Find "Delete" button on answers
- [ ] Click delete (confirm)
- [ ] Verify answer removed
- [ ] Test delete question feature

#### Test Analytics
- [ ] View teacher dashboard
- [ ] Check subject distribution chart
- [ ] Verify statistics are accurate
- [ ] Check recent questions list

### 4. Admin Features Testing

#### Test Admin Login
- [ ] Logout current user
- [ ] Login as: admin@askbuddy.com / admin123
- [ ] Verify admin dashboard appears
- [ ] Check all statistics display

#### Test Analytics Dashboard
- [ ] View admin dashboard
- [ ] Verify 6 stat cards display correctly
- [ ] Check subject distribution bar chart
- [ ] Verify top students table
- [ ] Check recent users table

#### Test User Management
- [ ] Click "Manage Users"
- [ ] Verify all users listed
- [ ] Test filter by role: Students
- [ ] Test filter by role: Teachers

#### Test Change User Role
- [ ] Find a student user
- [ ] Change role dropdown to "teacher"
- [ ] Verify role updated
- [ ] Change back to "student"

#### Test Delete User
- [ ] Find a test user
- [ ] Click delete button (trash icon)
- [ ] Confirm deletion
- [ ] Verify user removed from list
- [ ] Verify user's questions/answers removed

#### Test Content Moderation
- [ ] Browse questions
- [ ] Open any question
- [ ] Test delete answer feature
- [ ] Test delete question feature
- [ ] Verify content removed

### 5. Advanced Features Testing

#### Test Similar Question Detection
- [ ] Login as student
- [ ] Click "Ask New Question"
- [ ] Type title slowly: "What is photosynthesis"
- [ ] Wait 1 second
- [ ] Verify similar questions appear below
- [ ] Click on a similar question link
- [ ] Verify it opens in new tab

#### Test Reputation System
- [ ] Track initial reputation points
- [ ] Post an answer (+5 points)
- [ ] Get an upvote (+2 points)
- [ ] Get best answer (+15 points)
- [ ] Verify total matches expected

#### Test Search Functionality
- [ ] Go to Questions page
- [ ] Search: "Newton"
- [ ] Verify matching questions appear
- [ ] Search: "DNA"
- [ ] Verify results update

#### Test Image Upload
- [ ] Ask a new question
- [ ] Upload an image file
- [ ] Submit question
- [ ] Open question detail
- [ ] Verify image displays correctly

#### Test Responsive Design
- [ ] Resize browser window to mobile size
- [ ] Verify navbar collapses to hamburger menu
- [ ] Check cards stack vertically
- [ ] Test navigation on mobile view
- [ ] Verify all features work on mobile

### 6. Security Testing

#### Test Unauthorized Access
- [ ] Logout
- [ ] Try to access: /student/dashboard
- [ ] Verify redirect to login
- [ ] Login as student
- [ ] Try to access: /admin/dashboard
- [ ] Verify "Access denied" message

#### Test Role Permissions
- [ ] Login as student
- [ ] Verify no "Delete" buttons on others' content
- [ ] Verify can only mark best answer on own questions
- [ ] Login as teacher
- [ ] Verify can delete any answer
- [ ] Verify can mark any answer as best

#### Test SQL Injection Prevention
- [ ] Try login with: admin' OR '1'='1
- [ ] Verify login fails
- [ ] Try search with: '; DROP TABLE users; --
- [ ] Verify search works safely

### 7. Edge Cases Testing

#### Test Empty States
- [ ] Create new user with no activity
- [ ] Check dashboard shows "No questions posted"
- [ ] Check profile shows zero statistics
- [ ] Verify leaderboard includes new user

#### Test Long Content
- [ ] Post question with very long title (200+ chars)
- [ ] Post answer with 5000+ characters
- [ ] Verify content displays properly
- [ ] Check for text overflow issues

#### Test Special Characters
- [ ] Post question with title: "What is C++ vs C#?"
- [ ] Add tags with special chars: "c++, .net, #programming"
- [ ] Verify content saves and displays correctly

#### Test Duplicate Votes
- [ ] Upvote an answer
- [ ] Try to upvote same answer again
- [ ] Verify vote is removed (toggle behavior)
- [ ] Try downvote after upvote
- [ ] Verify vote changes

## Performance Testing

### Load Testing
- [ ] Create 50+ questions using seed script
- [ ] Browse questions page
- [ ] Verify page loads in < 2 seconds
- [ ] Test search with many results
- [ ] Check leaderboard with many users

### File Upload Testing
- [ ] Upload small image (< 1MB)
- [ ] Upload large image (10MB+)
- [ ] Upload PDF file (5MB)
- [ ] Verify file size limits enforced
- [ ] Check upload folder size

## Bug Reporting Template

If you find a bug, report it with:

```
**Bug Title:** Brief description

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Result:** What should happen

**Actual Result:** What actually happened

**User Role:** Student/Teacher/Admin

**Browser:** Chrome/Firefox/Safari

**Screenshot:** (if applicable)
```

## Test Completion Checklist

- [ ] All authentication tests passed
- [ ] All student features tested
- [ ] All teacher features tested
- [ ] All admin features tested
- [ ] Advanced features working
- [ ] Security tests passed
- [ ] Edge cases handled
- [ ] Performance acceptable
- [ ] No critical bugs found

## Success Criteria

✅ Users can register and login
✅ Students can post and answer questions
✅ Voting system works correctly
✅ Reputation points calculated accurately
✅ Teachers can moderate content
✅ Teachers can upload materials
✅ Admin can manage users
✅ Analytics display correctly
✅ Search and filters work
✅ Similar questions detected
✅ Images upload successfully
✅ Responsive on mobile devices
✅ No security vulnerabilities
✅ No data loss or corruption

---

**Happy Testing! 🧪**
