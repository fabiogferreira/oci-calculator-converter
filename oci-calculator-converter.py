import csv
import json
import uuid
import datetime
import argparse
import re

def generate_metadata():
    """Generate metadata section for the OCI Calculator JSON"""
    now = datetime.datetime.now(datetime.UTC)
    build_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return {
        "exportVersion": 1,
        "dataBuildID": {
            "buildDate": build_date,
            "buildNumber": 75,  # Default value from example
            "instance": "GEN2-PUBLIC-PROD",
            "realm": "public",
            "serviceType": "paas"
        },
        "hash": "0d0aa7cd2b2101bbcdaf6f32b4a5d148"  # Default value from example
    }

def create_vm_service(os_type, shape_name, ocpu_count, ram_gb, instances, service_ref):
    """Create a VM service configuration based on OS type and shape"""
    vm_service = {
        "id": 822,
        "label": "Compute - Virtual Machine",
        "utilization": {
            "instances": instances,
            "hours": 24,
            "days": 31,
            "hoursPerMonth": 744,
            "foreignInstanceMultiplier": {
                "value": 1,
                "description": ""
            }
        },
        "items": [
            {
                "sku": "B93113",  # SKU for VM.Standard.E4.Flex (from example)
                "quantity": ocpu_count,
                "minQuantity": 0,
                "unitPrice": 0.13778,
                "monthlyCost": 102.35 * instances
            },
            {
                "sku": "B93114",  # SKU for RAM
                "quantity": ram_gb,  # Usando RAM do CSV
                "minQuantity": 0,
                "unitPrice": 0.0082668,
                "monthlyCost": 49.13 * (ram_gb / 128) * instances  # Ajustando o cálculo para RAM e número de instâncias
            }
        ],
        "uiState": {
            "selectedOSExtended": os_type.lower(),
            "useReservedCapacity": False,
            "reservedCapacityPercentage": 0,
            "selectedCapacityType": "ondem"
        },
        "shapeName": shape_name,
        "shapeID": 3,  # Default from example
        "serviceRef": service_ref,
        "uuid": service_ref,
        "isFromShape": True
    }
    
    return vm_service

def create_block_storage(size_gb, performance_units, instances, service_ref):
    """Create a block storage service configuration"""
    block_service = {
        "id": 881,
        "label": "Storage - Block Volumes",
        "utilization": {
            "instances": instances,
            "hours": 24,
            "days": 31,
            "hoursPerMonth": 744,
            "foreignInstanceMultiplier": {
                "value": 1,
                "description": ""
            }
        },
        "items": [
            {
                "sku": "B91445",
                "quantity": 0,
                "minQuantity": 0,
                "unitPrice": 0,
                "monthlyCost": 0
            },
            {
                "sku": "B91961",  # SKU for block volume size
                "quantity": size_gb,
                "minQuantity": 0,
                "unitPrice": 0.1405356,
                "monthlyCost": round(0.1405356 * size_gb * instances, 2)
            },
            {
                "sku": "B91962",  # SKU for performance units
                "quantity": performance_units,
                "minQuantity": 0,
                "unitPrice": 0.00936904,
                "monthlyCost": round(0.00936904 * performance_units * instances, 2)
            }
        ],
        "uiState": {
            "hidePerformance": False,
            "hidePerformanceAndStorage": False,
            "forceFreeTier": False,
            "hideFreeTier": True,
            "freeTierApplied": False,
            "blockVolumesQty": size_gb,
            "vpuQty": performance_units // 100  # Assuming 10 VPUs per 1000 performance units
        },
        "presetID": 74,
        "customLabel": "Boot Volume",
        "serviceRef": service_ref,
        "isFromShape": False
    }
    
    return block_service

def create_windows_license(instances, service_ref):
    """Create a Windows license service configuration"""
    license_service = {
        "id": 827,
        "label": "Compute - OS Images",
        "utilization": {
            "instances": instances,
            "hours": 24,
            "days": 31,
            "hoursPerMonth": 744,
            "foreignInstanceMultiplier": {
                "value": 1,
                "description": ""
            }
        },
        "items": [
            {
                "sku": "B88318",
                "quantity": 1,
                "minQuantity": 1,
                "inPreset": True,
                "unitPrice": 0.5070304,
                "monthlyCost": 377.23 * instances
            }
        ],
        "uiState": {
            "selectedBurstableBaseline": "none"
        },
        "presetID": 74,
        "serviceRef": service_ref,
        "isFromShape": False
    }
    
    return license_service

def process_csv(csv_file):
    """Process CSV file and return OCI Calculator JSON"""
    configs = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            config_label = row['Label']
            os_type = row['OS']
            shape_name = row.get('Shape', 'VM.Standard.E4.Flex')
            ocpu_count = int(row.get('OCPU', 8))
            ram_gb = int(row.get('RAM_GB', ocpu_count * 16))  # Usa RAM_GB do CSV ou calcula como fallback
            storage_size = int(row.get('Storage_GB', 100))
            performance_units = int(row.get('Performance_Units', 1000))
            
            # Obter número de instâncias da coluna 'Qtd' ou 'Instances', com fallback para 1
            instances = 1
            if 'Qtd' in row:
                instances = int(row['Qtd'])
            elif 'Instances' in row:
                instances = int(row['Instances'])
            
            # Create unique service reference
            service_ref = str(uuid.uuid4())
            
            # Create services list for this configuration
            services = [
                create_vm_service(os_type, shape_name, ocpu_count, ram_gb, instances, service_ref),
                create_block_storage(storage_size, performance_units, instances, service_ref)
            ]
            
            # Add Windows license if OS is Windows
            if os_type.lower() == 'windows':
                services.append(create_windows_license(instances, service_ref))
            
            # Add configuration to configs list
            configs.append({
                "label": config_label,
                "services": services,
                "addBySearch": False
            })
    
    # Create final JSON structure
    result = {
        "label": "Generated Estimate",
        "timeFrame": {
            "months": 1,
            "from": None,
            "to": None,
            "leapYear": [],
            "calculation": "simple"
        },
        "currency": "BRL",
        "meta": generate_metadata(),
        "configs": configs
    }
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to OCI Calculator JSON')
    parser.add_argument('csv_file', help='Path to the input CSV file')
    parser.add_argument('--label', '-l', default='Generated Estimate', help='Estimate label')
    
    args = parser.parse_args()
    
    try:
        # Criar nome de arquivo baseado no label
        output_filename = re.sub(r'[^\w\-_]', '_', args.label) + '.json'
        
        result = process_csv(args.csv_file)
        result['label'] = args.label
        result['currency'] = 'BRL'  # Valor fixo para moeda BRL
        
        with open(output_filename, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Successfully generated OCI Calculator JSON: {output_filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
