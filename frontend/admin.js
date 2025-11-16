/**
 * Admin Dashboard JavaScript
 * Handles all admin-specific functionality
 */

function loadAdminDashboard() {
    console.log('Loading Admin Dashboard...');
    const app = document.getElementById('app');
    
    app.innerHTML = `
        <div style="padding: 40px; max-width: 1200px; margin: 0 auto; font-family: system-ui, -apple-system, sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                <h1 style="color: #4F46E5; margin: 0;">Admin Dashboard</h1>
                <button onclick="adminLogout()" style="padding: 10px 20px; background: #ef4444; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500;">Logout</button>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h2 style="margin: 0 0 15px 0; color: #1f2937;">Welcome, ${currentUser?.full_name || 'Administrator'}!</h2>
                <p style="color: #6b7280; margin: 5px 0;">📧 Email: ${currentUser?.email || ''}</p>
                <p style="color: #6b7280; margin: 5px 0;">👤 Role: Administrator</p>
            </div>
            
            <div style="background: #f0fdf4; padding: 30px; border-radius: 12px; border: 2px solid #86efac; margin-bottom: 20px;">
                <h3 style="margin: 0 0 15px 0; color: #15803d;">🎉 Deployment Successful!</h3>
                <p style="margin: 10px 0; color: #166534;">Your Smart Hiring System is now live on Render.com</p>
            </div>
            
            <div style="background: #fef3c7; padding: 30px; border-radius: 12px; border: 2px solid #fbbf24;">
                <h3 style="margin: 0 0 15px 0; color: #92400e;">⚠️ Feature Status</h3>
                <p style="margin: 10px 0; color: #78350f; font-size: 14px;">
                    <strong>Note:</strong> Some features are temporarily disabled due to deployment size constraints
                </p>
                <ul style="margin-top: 15px; color: #78350f; font-size: 14px; line-height: 1.8;">
                    <li>✅ <strong>Authentication System</strong> - Active</li>
                    <li>✅ <strong>Job Management</strong> - Active</li>
                    <li>✅ <strong>Candidate Management</strong> - Active</li>
                    <li>⚠️ <strong>Assessment System</strong> - Disabled (ML libraries removed)</li>
                    <li>⚠️ <strong>Dashboard Analytics</strong> - Disabled (pandas removed)</li>
                    <li>⚠️ <strong>PDF/DOCX Resume Parsing</strong> - Disabled (size constraints)</li>
                </ul>
            </div>
            
            <div style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h3 style="margin: 0 0 20px 0; color: #1f2937;">📊 Quick Stats</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                    <div style="background: #f3f4f6; padding: 20px; border-radius: 8px;">
                        <div style="color: #6b7280; font-size: 14px; margin-bottom: 5px;">Total Users</div>
                        <div style="font-size: 28px; font-weight: bold; color: #4F46E5;">--</div>
                    </div>
                    <div style="background: #f3f4f6; padding: 20px; border-radius: 8px;">
                        <div style="color: #6b7280; font-size: 14px; margin-bottom: 5px;">Active Jobs</div>
                        <div style="font-size: 28px; font-weight: bold; color: #10b981;">--</div>
                    </div>
                    <div style="background: #f3f4f6; padding: 20px; border-radius: 8px;">
                        <div style="color: #6b7280; font-size: 14px; margin-bottom: 5px;">Applications</div>
                        <div style="font-size: 28px; font-weight: bold; color: #f59e0b;">--</div>
                    </div>
                </div>
                <p style="margin-top: 20px; color: #9ca3af; font-size: 13px; text-align: center;">
                    Full admin features will be implemented in the next phase
                </p>
            </div>
        </div>
    `;
}

function adminLogout() {
    // Clear authentication data
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('currentRole');
    
    // Reload the page to return to login
    window.location.href = '/';
}
