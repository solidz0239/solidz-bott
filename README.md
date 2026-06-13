 🤖 SolidZ Discord Bot

Discord bot for license activation, ticket system, leveling, and server management.

## 🚀 Commands

### License System
| Command | Description |
|---------|-------------|
| `!activate <key>` | Activate your license (DM only) |
| `!status` | Check your license status |
| `!gen <product> <duration>` | Generate license (Owner only) |

### Products
| Command | Description |
|---------|-------------|
| `!tweaker` | Tweaker download link |
| `!spoofer` | Spoofer download link |
| `!buy` | Purchase information |
| `!prices` | Show all prices |

### Support
| Command | Description |
|---------|-------------|
| `!ticket <reason>` | Create support ticket |
| `!close` | Close ticket |
| `!verify` | Get verified role |

### Leveling
| Command | Description |
|---------|-------------|
| `!rank [@user]` | Check your level rank |
| `!leaderboard` | Top 10 level leaderboard |

### Staff
| Command | Description |
|---------|-------------|
| `!kick <@user>` | Kick member |
| `!ban <@user>` | Ban member |
| `!clear <amount>` | Clear messages |

### Owner
| Command | Description |
|---------|-------------|
| `!create` | Create full server (100+ roles, 80+ channels) |
| `!destroy` | Destroy server |

## 🔧 Setup

1. Install Python 3.12+
2. Install dependencies:
   ```bash
   pip install discord.py
