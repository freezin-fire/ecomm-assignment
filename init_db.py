import sqlite3
import os

DB_NAME = "ecommerce.db"

SAMPLE_PRODUCTS = [
    (
        "Ant Esports ICE-112 Mid-Tower Gaming Cabinet",
        "Mid-Tower gaming case featuring high-airflow mesh front panel, 4 pre-installed 120mm rainbow LED fans, tempered glass side panel, and support for ATX, Micro-ATX, and Mini-ITX motherboards.",
        3299.00,
        "Cabinet",
        "/static/images/ant-esports-cabinet.jpg",
        4.6
    ),
    (
        "Zebronics Zeb-Cronus Premium Gaming Chassis",
        "Premium chassis with front and side tempered glass panels, 4x 120mm dual-ring RGB fans, dual USB 3.0 ports, heavy-duty steel structure, and optimized airflow path.",
        2999.00,
        "Cabinet",
        "/static/images/zeb-cabinet.jpg",
        4.4
    ),
    (
        "Cooler Master MasterBox Q300L Micro-ATX Case",
        "Modular Micro-ATX tower with patterned magnetic dust filters, edge-to-edge transparent side panel, movable I/O panel, and support for standard ATX PSUs.",
        3999.00,
        "Cabinet",
        "/static/images/cooler-master-cabinet.jpg",
        4.7
    ),

    (
        "MSI B550M PRO-VDH WiFi Motherboard",
        "AMD AM4 Micro-ATX motherboard with PCIe 4.0 support, dual M.2 with Shield Frozr, Wi-Fi 5, Bluetooth 4.2, DDR4 Boost up to 4400MHz, and Core Boost technology.",
        9499.00,
        "Motherboard",
        "/static/images/msi-motherboard.jpg",
        4.7
    ),
    (
        "Gigabyte B760M DS3H AX DDR4 Motherboard",
        "Intel LGA1700 motherboard for 12th, 13th, and 14th Gen Core CPUs, dual PCIe 4.0 M.2 slots, Intel Wi-Fi 6E, 2.5GbE LAN, and USB 3.2 Gen 2 Type-C.",
        11990.00,
        "Motherboard",
        "/static/images/gigabyte-motherboard.jpg",
        4.6
    ),
    (
        "ASUS Prime H610M-E D4 Motherboard",
        "Budget LGA1700 micro-ATX board with 32Gbps M.2 slot, Realtek 1Gb Ethernet, HDMI/DP/VGA ports, DIGI+ VRM, and ASUS 5X Protection III hardware safeguards.",
        6799.00,
        "Motherboard",
        "/static/images/asus-motherboard.jpg",
        4.3
    ),

    (
        "AMD Ryzen 5 5600X Desktop Processor",
        "6 Cores and 12 processing threads, 4.6 GHz Max Boost clock, 35MB Cache, Socket AM4, PCIe 4.0 support, bundled with AMD Wraith Stealth cooler.",
        12899.00,
        "CPU",
        "/static/images/amd-ryzen-5-5600x.jpg",
        4.8
    ),
    (
        "Intel Core i5-12400F 12th Gen Processor",
        "6 Performance cores and 12 threads, up to 4.4 GHz Turbo Boost, LGA1700 socket, 18MB Intel Smart Cache, PCIe 5.0 and DDR5/DDR4 memory support.",
        10499.00,
        "CPU",
        "/static/images/intel-i5-12400f.jpg",
        4.8
    ),
    (
        "AMD Ryzen 7 5700X Desktop Processor",
        "8 Cores and 16 processing threads, 4.6 GHz Max Boost, 36MB GameCache, AM4 socket, 65W energy efficient TDP for elite content creation and high-FPS gaming.",
        16499.00,
        "CPU",
        "/static/images/amd-ryzen-7-5700x.jpg",
        4.9
    ),

    (
        "ZOTAC Gaming GeForce RTX 4060 8GB Twin Edge",
        "NVIDIA Ada Lovelace architecture, 8GB GDDR6, DLSS 3 AI frame generation, full ray tracing, IceStorm 2.0 dual 90mm fans, and compact form factor.",
        28999.00,
        "GPU",
        "/static/images/zotac-gpu.jpg",
        4.7
    ),
    (
        "MSI GeForce RTX 3050 Ventus 2X 8GB OC",
        "8GB GDDR6 128-bit memory, TORX Fan 3.0 dual cooling design, custom reinforced backplate, Ray Tracing Cores, and DLSS AI acceleration for 1080p gaming.",
        19999.00,
        "GPU",
        "/static/images/msi-gpu.jpg",
        4.5
    ),
    (
        "Gigabyte Radeon RX 6600 Eagle 8GB",
        "AMD RDNA 2 architecture with 8GB GDDR6, WINDFORCE 3X cooling system with alternate spinning fans, screen cooling, and full DirectX 12 Ultimate support.",
        21499.00,
        "GPU",
        "/static/images/gigabyte-gpu.jpg",
        4.6
    ),

    (
        "Corsair Vengeance LPX 16GB (1x16GB) DDR4 3200MHz",
        "Pure aluminum heat spreader for ultra-fast thermal dissipation, custom high-performance PCB, low profile form factor, Intel XMP 2.0 automatic overclocking.",
        3299.00,
        "RAM",
        "/static/images/corsair-ram.jpg",
        4.7
    ),
    (
        "Crucial RAM 8GB DDR4 3200MHz Desktop Memory",
        "CL22 1.2V low power memory module, plug-and-play desktop RAM upgrade engineered to run faster and smoother for reliable multitasking.",
        1499.00,
        "RAM",
        "/static/images/crucial-ram.jpg",
        4.5
    ),
    (
        "G.Skill Ripjaws V 16GB (2x8GB) DDR4 3600MHz CL18",
        "Dual-channel high-speed memory kit, aggressive aluminum fin heat spreader, rigorous testing across major motherboard platforms for maximum reliability.",
        3999.00,
        "RAM",
        "/static/images/gskill-ram.jpg",
        4.8
    ),

    (
        "Redragon K552 Kumara RGB Mechanical Gaming Keyboard",
        "Tenkeyless 87-key compact mechanical keyboard with custom clicky blue switches, 18 vibrant RGB backlighting modes, splash-proof design, and anti-ghosting.",
        2799.00,
        "Keyboard",
        "/static/images/redragon-keyboard.jpg",
        4.6
    ),
    (
        "Cosmic Byte CB-GK-16 Firefly Mechanical Keyboard",
        "Outemu blue tactile mechanical switches, per-key RGB backlighting, braided durable cable, compact TKL layout, and lightweight aluminum faceplate.",
        2199.00,
        "Keyboard",
        "/static/images/cosmic-byte-keyboard.jpg",
        4.4
    ),
    (
        "Logitech G213 Prodigy Gaming Keyboard",
        "Mech-Dome keys tuned to deliver tactile feedback comparable to mechanical switches, customizable 5-zone RGB lighting with LIGHTSYNC, and spill resistance.",
        3795.00,
        "Keyboard",
        "/static/images/logitech-keyboard.jpg",
        4.5
    ),

    (
        "Logitech G102 Lightsync Optical Gaming Mouse",
        "Gaming-grade 8,000 DPI sensor, customizable RGB color wave lighting, 6 programmable buttons, and mechanical spring button tensioning for consistent clicks.",
        1495.00,
        "Mouse",
        "/static/images/logitech-mouse.jpg",
        4.7
    ),
    (
        "Razer DeathAdder Essential Gaming Mouse",
        "Proven ergonomic form factor, 6,400 DPI optical sensor, 5 Hyperesponse buttons, multi-award winning design, mechanical switches rated up to 10M clicks.",
        1299.00,
        "Mouse",
        "/static/images/razer-mouse.jpg",
        4.5
    ),
    (
        "Redragon M601 RGB Centrophorus Gaming Mouse",
        "Adjustable 3,200 DPI sensor, 6 optimized buttons with anti-skid scroll wheel, 8-piece weight tuning set (2.4g x 8), and smooth durable Teflon feet pads.",
        899.00,
        "Mouse",
        "/static/images/redragon-mouse.jpg",
        4.3
    ),

    (
        "Logitech Z120 USB Stereo Speakers",
        "Compact 2.0 multimedia stereo speakers with USB power connection and 3.5mm audio input, integrated power and volume knob, and clean cord management.",
        1195.00,
        "Speakers",
        "/static/images/logitech-speakers.jpg",
        4.5
    ),
    (
        "Zebronics Zeb-Warrior 2.0 Multimedia Speakers",
        "USB powered desktop speakers featuring pulsating RGB breathing lights, 3.5mm AUX jack input, rotary volume control, and 10W RMS stereo output.",
        699.00,
        "Speakers",
        "/static/images/zebronics-speakers.jpg",
        4.2
    ),
    (
        "Creative Pebble 2.0 USB Desktop Speakers",
        "Custom-tuned 45-degree elevated soundstage drivers, rear-facing passive radiators for rich bass, front-panel volume knob, and modern minimalist spherical design.",
        1899.00,
        "Speakers",
        "/static/images/creative-speakers.jpg",
        4.7
    ),

    (
        "Cosmic Byte GS410 Gaming Headphone with Mic",
        "Soft cushioned earcups and headband, flexible high-sensitivity microphone, 40mm neodymium drivers for clear bass audio, 3.5mm single jack with PC splitter.",
        899.00,
        "Headphones",
        "/static/images/cosmic-byte-headphones.jpg",
        4.3
    ),
    (
        "HyperX Cloud Stinger 2 Gaming Headset",
        "Lightweight comfortable design, 50mm directional drivers, DTS Headphone:X Spatial Audio 2-year activation code, swivel-to-mute noise-canceling microphone.",
        3490.00,
        "Headphones",
        "/static/images/hyperx-headset.jpg",
        4.6
    ),
    (
        "boAt Rockerz 550 Over-Ear Wireless Headphones",
        "50mm dynamic audio drivers, up to 20 hours battery playback, ergonomic earcups with physical volume buttons, Bluetooth 5.0 and AUX dual mode.",
        1999.00,
        "Headphones",
        "/static/images/boat-headphones.jpg",
        4.4
    ),

    (
        "Redgear Pro Wireless Gamepad",
        "2.4GHz wireless technology with 10-meter range, dual vibration force feedback, illuminated backlit keys, and built-in rechargeable battery lasting up to 10 hours.",
        1499.00,
        "Game Controllers",
        "/static/images/redgear-gamepad.jpg",
        4.4
    ),
    (
        "Cosmic Byte Nebula Wireless Gamepad",
        "Compatible with PC (Windows 10/11) and Android, dual vibration motors, magnetic responsive analog triggers, textured non-slip grips, and low latency connection.",
        1899.00,
        "Game Controllers",
        "/static/images/cosmic-byte-gamepad.jpg",
        4.3
    ),
    (
        "Microsoft Xbox Wireless Controller (Carbon Black)",
        "Refined ergonomic geometry, hybrid D-pad, textured grip on triggers and bumpers, seamless Bluetooth pairing across Windows PC, Xbox, Android, and iOS.",
        5390.00,
        "Game Controllers",
        "/static/images/microsoft-xbox-controller.jpg",
        4.8
    )
]

def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DB_NAME)
    schema_path = os.path.join(base_dir, "schema.sql")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    cursor.executemany(
        """
        INSERT INTO products (name, description, price, category, image_url, rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        SAMPLE_PRODUCTS
    )

    conn.commit()
    conn.close()
    print(f"Database initialized and seeded successfully with {len(SAMPLE_PRODUCTS)} products: {db_path}")

if __name__ == "__main__":
    init_db()
