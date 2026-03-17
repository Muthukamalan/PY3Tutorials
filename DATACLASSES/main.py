from datetime import datetime,timezone
from dataclasses import dataclass, field,replace,asdict,astuple,InitVar

from typing import Optional,Any
import csv 
import io
from warnings import filterwarnings
filterwarnings("ignore")


# ====================== reduce boilerplate =================================================================
@dataclass
class User:
    """A user in the system."""
    name: str
    email: str
    age: int


user1 = User(name="Alice", email="alice@example.com", age=1000)
print(user1)

# ------------------------------------------------------------------------------------------------------------

class NormalUser:
    def __init__(self,name,email,age):
        self.name  = name 
        self.email = email 
        self.age = age 

    def __repr__(self):
        return f"NormalUser(name={self.name!r}, email={self.email!r}, age={self.age})"
    def __eq__(self, other):
        if not isinstance(other, NormalUser):
            return NotImplemented
        return (self.name, self.email, self.age) == (other.name, other.email, other.age)

user2 = NormalUser("abdhul","isaac@proton.mail",age=90)
print(user2)

# ================================ InitVar, __post_init__ ======================================================



@dataclass
class Product:
    """Product with field metadata for validation."""
    name: str 
    # Initvar - passed to __init__ but not stored as field
    provider: InitVar[str]
    price: float = field(metadata={'min': 0, 'currency': 'USD'})
    quantity: int = field(metadata={'min': 0},default=0)
    tags:list[str] = field(default_factory=list)
    uploaded_at: datetime = field(init=False,default_factory=datetime.now,repr=True)
    pid:str = field(init=False,repr=False)

    
    def __post_init__(self,provider:str):
        """Called after the auto-generated __init__."""
        # InitVar should pass it on __post__init__
        # Calculate derived values
        if self.price<0:
            raise ValueError


chair = Product(name="chair",provider="valueMart",price=132.3)
pc = Product(name="ASUS Gaming PC",provider="DMart",price=323,quantity=10,tags=["wood","wheels"])

print(chair)
print(pc)

# ================================ Frozen, Slots, Ordered, replace ======================================================

#  Frozen dataclasses cannot be modified;  
#  Frozen dataclasses can be used in sets and as dict keys
@dataclass(frozen=True,slots=True)
class Point:
    """An immutable 2D point."""
    x: float
    y: float
    debug:bool = field(init=True,default=False)

    def with_debug(self,debug:bool)->'Point':
        return replace(self,debug=True)
    
    @property
    def coordinate(self)->str:
        return f"{self.x},{self.y} is my co-ordinate"
    
    def magnitude(self)->float:
        return (self.x **2 + self.y ** 2) ** 0.5

point = Point(3.0, 4.0)
print(f"{point.coordinate=}")
print(f"{point.magnitude()=}")

try:
    point.x = 5.0  # This raises an error
except AttributeError as e:
    print(f"Cannot modify frozen dataclass: {e}")

points = {Point(0, 0), Point(1, 1), Point(0, 0)}  # Only because it's frozen
print(f"{len(points)=}")  # 2 - duplicates removed


dup_point = point.with_debug(True) # original unchanged
print(dup_point)

# ====================================== Inheritance ========================================================


@dataclass
class BaseModel:
    """Base class for all database models."""
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

@dataclass
class User(BaseModel):
    """User model extending BaseModel."""
    username: str = ""  # Default required because parent has defaults
    email: str = ""
    is_active: bool = True

@dataclass
class Admin(User):
    """Admin user with additional permissions."""
    permissions: list = field(default_factory=list)
    access_level: int = 1




# Create instances
user = User(username="alice", email="alice@example.com")
print(user.id)  # None - inherited from BaseModel
print(user.created_at)  # Current timestamp

admin = Admin(
    username="admin",
    email="admin@example.com",
    permissions=["read", "write", "delete"],
    access_level=10
)
print(admin)


admin_dict = asdict(admin)
# ==============================================================================================





@dataclass
class LogEntry:
    """
    Log entry with multiple construction methods.
    
    Demonstrates factory methods for creating instances
    from various data sources.
    """
    timestamp: datetime
    level: str
    message: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def create(cls,level: str,message: str,source: str = "app",**metadata) -> "LogEntry":
        """
        Convenient factory with auto-timestamp.
        
        Usage:
            log = LogEntry.create("INFO", "User logged in", user_id=123)
        """
        return cls(timestamp=datetime.now(),level=level.upper(),message=message,source=source,metadata=metadata)
    
    @classmethod
    def from_string(cls, log_line: str) -> "LogEntry":
        """
        Parse from common log format string.
        
        Expected format: "2024-01-15T10:30:00 [INFO] source: message"
        """
        # Parse timestamp
        timestamp_str, rest = log_line.split(" [", 1)
        timestamp = datetime.fromisoformat(timestamp_str)
        
        # Parse level
        level, rest = rest.split("] ", 1)
        
        # Parse source and message
        source, message = rest.split(": ", 1)
        
        return cls(timestamp=timestamp,level=level,message=message,source=source)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LogEntry":
        """Create from dictionary (e.g., JSON parsed data)."""
        # Handle timestamp string conversion
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        
        return cls(**data)
    
    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "LogEntry":
        """Create from CSV row dictionary."""
        # CSV doesn't support nested data
        return cls(timestamp=datetime.fromisoformat(row["timestamp"]),level=row["level"],message=row["message"],source=row["source"],metadata={})
    
    @classmethod
    def batch_from_csv(cls, csv_content: str) -> list:
        """Parse multiple entries from CSV content."""
        reader = csv.DictReader(io.StringIO(csv_content))
        return [cls.from_csv_row(row) for row in reader]
    
    def format(self) -> str:
        """Format log entry for output."""
        return f"{self.timestamp.isoformat()} [{self.level}] {self.source}: {self.message}"


# Different ways to create LogEntry instances

# 1. Direct construction
log1 = LogEntry( timestamp=datetime.now(),level="ERROR",message="Connection failed",source="database")

# 2. Convenient factory
log2 = LogEntry.create("INFO", "User logged in", user_id=123, ip="192.168.1.1")

# 3. Parse from string
log_line = "2024-01-15T10:30:00 [WARN] auth: Invalid token"
log3 = LogEntry.from_string(log_line)

# 4. From dictionary (e.g., JSON data)
log4 = LogEntry.from_dict({"timestamp": "2024-01-15T11:00:00","level": "DEBUG","message": "Cache miss","source": "cache","metadata": {"key": "user:123"}})

# 5. Batch from CSV
csv_data = """timestamp,level,message,source
2024-01-15T12:00:00,INFO,Request started,api
2024-01-15T12:00:01,INFO,Request completed,api"""

logs = LogEntry.batch_from_csv(csv_data)

print("Created logs:")
for log in [log1, log2, log3, log4] + logs:
    print(f"  {log.format()}")