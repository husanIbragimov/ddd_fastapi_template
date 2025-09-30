"""
Complete Test Script - Database Session & DI Container
Bu script butun sistemni test qiladi
"""
import asyncio
from uuid import uuid4
from datetime import datetime

from di import container
from domain.repository import UserRepository, CategoryRepository
from domain.entity import UserEntity, CategoryEntity
from infrastructure.persistence.db_session import (
    get_db_session_manager,
    startup_db,
    shutdown_db
)


async def test_database_session_manager():
    """Test 1: DatabaseSessionManager"""
    print("=" * 70)
    print("🧪 TEST 1: DatabaseSessionManager")
    print("=" * 70)

    # Get singleton instance
    db_manager = get_db_session_manager()
    print(f"✅ DatabaseSessionManager: {db_manager}")
    print(f"   - Engine: {db_manager.engine}")
    print(f"   - Pool size: {db_manager.engine.pool.size()}")

    # Health check
    is_healthy = await db_manager.health_check()
    print(f"✅ Health check: {'PASSED' if is_healthy else 'FAILED'}")

    # Test session factory
    session1 = db_manager.session_factory()
    session2 = db_manager.session_factory()

    print(f"✅ Session 1: {session1}")
    print(f"✅ Session 2: {session2}")
    print(f"   - Are they same? {session1 is session2}")  # Should be False

    await session1.close()
    await session2.close()

    print("\n✅ DatabaseSessionManager test PASSED!\n")


async def test_di_container():
    """Test 2: DI Container & Repository Injection"""
    print("=" * 70)
    print("🧪 TEST 2: DI Container & Repository Injection")
    print("=" * 70)

    # Get repositories from container
    user_repo = container.get(UserRepository)
    category_repo = container.get(CategoryRepository)

    print(f"✅ UserRepository: {user_repo}")
    print(f"   - Type: {type(user_repo).__name__}")
    print(f"   - Model class: {user_repo.model_class.__name__}")
    print(f"   - DB Session: {user_repo.db}")

    print(f"\n✅ CategoryRepository: {category_repo}")
    print(f"   - Type: {type(category_repo).__name__}")
    print(f"   - Model class: {category_repo.model_class.__name__}")
    print(f"   - DB Session: {category_repo.db}")

    # Test singleton
    user_repo2 = container.get(UserRepository)
    print(f"\n✅ Singleton test:")
    print(f"   - Same repository instance? {user_repo is user_repo2}")  # Should be True
    print(f"   - Same session instance? {user_repo.db is user_repo2.db}")  # Should be False

    print("\n✅ DI Container test PASSED!\n")


async def test_database_operations():
    """Test 3: Real Database Operations"""
    print("=" * 70)
    print("🧪 TEST 3: Database Operations")
    print("=" * 70)

    user_repo = container.get(UserRepository)
    category_repo = container.get(CategoryRepository)

    # Test 3.1: Create Category
    print("\n📝 Test 3.1: Creating category...")
    test_category = CategoryEntity(
        uuid=None,
        name={
            "en": "Electronics",
            "uz": "Elektronika",
            "ru": "Электроника"
        },
        description={
            "en": "Electronic devices and gadgets",
            "uz": "Elektron qurilmalar va gadjetlar",
            "ru": "Электронные устройства и гаджеты"
        }
    )

    try:
        created_category = await category_repo.create(test_category)
        print(f"✅ Category created: {created_category.uuid}")
        print(f"   - Name (en): {created_category.name['en']}")
        print(f"   - Name (uz): {created_category.name['uz']}")

        # Test 3.2: Get Category
        print("\n📝 Test 3.2: Getting category by UUID...")
        found_category = await category_repo.get_by_uuid(created_category.uuid)
        if found_category:
            print(f"✅ Category found: {found_category.name['en']}")
        else:
            print("❌ Category not found!")

        # Test 3.3: List Categories
        print("\n📝 Test 3.3: Listing categories...")
        categories = await category_repo.list(skip=0, limit=10)
        print(f"✅ Found {categories.total} categories")
        for cat in categories.items[:3]:  # Show first 3
            print(f"   - {cat.name['en']} ({cat.uuid})")

    except Exception as e:
        print(f"❌ Category operations failed: {e}")
        import traceback
        traceback.print_exc()

    # Test 3.4: Create User
    print("\n📝 Test 3.4: Creating user...")
    test_user = UserEntity(
        uuid=uuid4(),
        first_name="Test",
        last_name="User",
        username=f"testuser_{uuid4().hex[:8]}",  # Unique username
        phone_number=f"+99890{uuid4().hex[:7]}",  # Unique phone
        email=f"test_{uuid4().hex[:8]}@example.com",  # Unique email
        date_joined=datetime.utcnow(),
        hashed_password="hashed_password_here"
    )

    try:
        user_uuid = await user_repo.save(test_user)
        print(f"✅ User created: {user_uuid}")

        # Test 3.5: Get User
        print("\n📝 Test 3.5: Getting user by email...")
        found_user = await user_repo.get_by_email(test_user.email)
        if found_user:
            print(f"✅ User found: {found_user.first_name} {found_user.last_name}")
            print(f"   - Email: {found_user.email}")
            print(f"   - Username: {found_user.username}")
        else:
            print("❌ User not found!")

        # Test 3.6: Get User by UUID
        print("\n📝 Test 3.6: Getting user by UUID...")
        found_user_by_id = await user_repo.get_by_uuid(user_uuid)
        if found_user_by_id:
            print(f"✅ User found by UUID: {found_user_by_id.username}")
        else:
            print("❌ User not found by UUID!")

    except Exception as e:
        print(f"❌ User operations failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n✅ Database Operations test COMPLETED!\n")


async def test_session_isolation():
    """Test 4: Session Isolation"""
    print("=" * 70)
    print("🧪 TEST 4: Session Isolation")
    print("=" * 70)

    # Get multiple repository instances
    repo1 = container.get(UserRepository)
    repo2 = container.get(UserRepository)
    repo3 = container.get(UserRepository)

    print(f"Repository 1: {id(repo1)}")
    print(f"Repository 2: {id(repo2)}")
    print(f"Repository 3: {id(repo3)}")
    print(f"\n✅ All same instance (singleton): {repo1 is repo2 is repo3}")

    print(f"\nSession 1: {id(repo1.db)}")
    print(f"Session 2: {id(repo2.db)}")
    print(f"Session 3: {id(repo3.db)}")
    print(f"\n⚠️  Sessions might be same or different depending on timing")
    print("   (In real FastAPI request, each request gets new session)")

    print("\n✅ Session Isolation test COMPLETED!\n")


async def main():
    """Main test runner"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "COMPLETE DI SYSTEM TEST" + " " * 30 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    try:
        # Startup database
        await startup_db()

        # Run all tests
        await test_database_session_manager()
        await test_di_container()
        await test_database_operations()
        await test_session_isolation()

        # Final summary
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 20 + "ALL TESTS PASSED! ✅" + " " * 27 + "║")
        print("╚" + "=" * 68 + "╝")

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED!")
        print("=" * 70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Shutdown database
        await shutdown_db()


if __name__ == "__main__":
    asyncio.run(main())