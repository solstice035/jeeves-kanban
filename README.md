# Jeeves Task Board

Beautiful, self-hosted Kanban board for managing Jeeves tasks and collaboration.

## 🚀 Quick Start

### Local Access (Single Computer)

1. **Open the board:**
   ```bash
   open /Users/nick/clawd/jeeves-kanban/index.html
   ```
   Or simply double-click `index.html` in Finder

2. **Start using:**
   - Drag cards between columns
   - Click "+ Add Task" to create new tasks
   - Add descriptions and tags to organize work
   - Everything auto-saves to browser localStorage

### 🌐 Network Access (All Devices)

**Access from phone, tablet, or any device on your network:**

1. **Start the server:**
   ```bash
   cd /Users/nick/clawd/jeeves-kanban
   ./start-server.sh
   ```

2. **Access from any device:**
   - **This computer:** http://localhost:8888/
   - **Other devices:** http://192.168.1.224:8888/
   
   Replace `192.168.1.224` with your actual local IP (shown when server starts)

3. **Stop the server:**
   ```bash
   ./stop-server.sh
   ```

**Features:**
- ✅ Access from any device on your local network
- ✅ Phone-friendly responsive design
- ✅ Real-time updates via localStorage
- ✅ Secure (local network only, no internet exposure)

## ✨ Features

- **Beautiful UI**: Modern gradient design with smooth animations
- **Drag & Drop**: Intuitive card movement between columns
- **Tags**: Categorize tasks with custom tags
- **Auto-Save**: All changes saved automatically
- **Export/Import**: Backup your board data as JSON
- **Self-Hosted**: Runs 100% locally, no external services
- **No Setup**: Just open the HTML file - no installation needed

## 📋 Board Columns

1. **📥 Backlog** - Ideas and future tasks
2. **✅ Ready** - Prepared and ready to start
3. **🚀 In Progress** - Currently being worked on
4. **👀 Review** - Completed, awaiting review
5. **🎉 Done** - Completed tasks

## 🎯 Pre-Loaded Tasks

The board comes pre-loaded with the overnight challenge tasks:

- Phase 1: Project Intelligence Dashboard
- Phase 2: Meeting Intelligence System
- Phase 3: Client Intelligence Briefs
- Phase 4: Automation Scripts
- Phase 5: Vault Intelligence Report
- Phase 6: Enhanced Personal Skills

## 💾 Data Management

### Export Board
Click "💾 Export Data" to save board as JSON file

### Import Board
Click "📥 Import Data" to restore from JSON backup

### Clear Board
Click "🗑️ Clear Board" to start fresh (with confirmation)

## 🔄 Integration with Obsidian

A parallel Kanban board exists in Obsidian:
- Location: `/Users/nick/obsidian/claude/Jeeves Task Board.md`
- Syncs manually (copy tasks between boards as needed)
- Uses Obsidian Kanban plugin format

## 🛠️ Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript
- **Storage**: Browser localStorage
- **Dependencies**: None - completely self-contained
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

## 📱 Usage Tips

1. **Workflow**: Backlog → Ready → In Progress → Review → Done
2. **Tags**: Use consistent tags for filtering (e.g., `urgent`, `client-work`, `automation`)
3. **Descriptions**: Add context to help remember task details
4. **Regular Exports**: Backup your board weekly using Export function
5. **Collaboration**: Share exported JSON files to sync board state

## 🎨 Customization

Edit the CSS in `index.html` to customize:
- Colors and gradients
- Column names and emoji
- Card styling
- Animations

## 📝 Notes

- Data persists in browser localStorage (tied to file location)
- Moving the HTML file will reset the board (export/import to migrate)
- For shared access, consider hosting on local web server
- Compatible with Canvas app for presenting the board

## 🔗 Quick Links

- **Obsidian Board**: [[Jeeves Task Board]]
- **Project Folder**: `/Users/nick/clawd/jeeves-kanban/`
- **Backup Location**: Export to `/Users/nick/clawd/jeeves-kanban/backups/`

---

**Created**: 2026-01-29  
**Version**: 1.0  
**Status**: Production Ready ✅
