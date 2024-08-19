import pandas as pd

def get_suppliers_and_ids(dataframe):
    suppliers_and_ids = []
    
    for index, row in dataframe.iterrows():
        collection = [row['COLLECTION'].split("_")[0] + '___' + row['COMPOUND_ID']]
        duplicates = [(string.split('_')[0] + '___' + string.split()[-1]) for string in row['DUPLICATES'].split(',') if string != 'none']
        suppliers_and_ids.append(collection + duplicates)
    
    return suppliers_and_ids

def move_to_front(item_list, value):
    
    for item in item_list:        
        if value in item:
            item_list.remove(item)
            item_list.insert(0, item)
    
    return item_list

def custom_list_sort(nested_item_list, keywords):
    nested_list = [sorted(set(item_list)) for item_list in nested_item_list]

    for item_list in nested_list:
        for keyword in keywords:
            item_list = move_to_front(item_list, keyword)
    
    return nested_list

def get_preferred_suppliers(suppliers_and_ids):
    preferred_supplier = [string[0].split('___')[0] for string in suppliers_and_ids]
    return preferred_supplier

def get_preferred_ids(suppliers_and_ids):
    preferred_id = [string[0].split('___')[-1] for string in suppliers_and_ids]
    return preferred_id

def get_df_order(unordered_list, priority_items):
    ordered_list = sorted(set(unordered_list))
    
    for item in priority_items:
        move_to_front(ordered_list, item)

    return ordered_list


### --- MAKE SURE YOU HAVE OPENED THE ENTIRE FOLDER IN VSCode --- ###
### --- MAKE SURE INPUT FILE IS IN THE SAME FOLDER --- ###
### --- CHANGE input_file TO INPUT FILE NAME --- ### 
### --- MAKE SURE INPUT FILE IS NOT OPEN WHEN RUNNING --- ###

input_file = 'Data.xlsx'
supplier_df = pd.read_excel(input_file)
priority_suppliers = ['MolPort', 'Enamine']

sorted_suppliers_and_ids = custom_list_sort(get_suppliers_and_ids(supplier_df), priority_suppliers)
preferred_suppliers = get_preferred_suppliers(sorted_suppliers_and_ids)
preferred_ids = get_preferred_ids(sorted_suppliers_and_ids)
all_suppliers = [', '.join(row) for row in sorted_suppliers_and_ids]

data = {'PREFERRED_SUPPLIER': preferred_suppliers, 
        'PREFFERED_ID': preferred_ids, 
        'ALL_SUPPLIERS': all_suppliers,
        'CRESSET_ID': supplier_df['CRESSET_ID'], 
        'Smiles': supplier_df['Smiles']
        }

new_df = pd.DataFrame(data)

supplier_order = get_df_order(preferred_suppliers, priority_suppliers)
new_df['PREFERRED_SUPPLIER'] = pd.Categorical(new_df['PREFERRED_SUPPLIER'], categories = supplier_order)
new_df.sort_values(by = 'PREFERRED_SUPPLIER', inplace=True)
new_df.head()

### --- CHANGE output_file to OUTPUT FILE NAME --- ###
output_file = 'Result.xlsx'
new_df.to_excel(output_file, index=False)