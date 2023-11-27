#include<stdio.h>
#include<string.h> 
#include<stdbool.h>

#include<Python.h>

static PyObject* loads(PyObject* self, PyObject* args) {
    PyObject* dict = NULL;
    if(!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    const char* json_string;
    if(!PyArg_ParseTuple(args, "s", &json_string)) {
        printf("ERROR: Failed to parse string\n");
        return NULL;
    }

    const char* token_start;
    const char* token_end = json_string;
    
    while(1) {
        // parse key
        token_start = strchr(token_end, '\"');
        if(token_start == NULL) {
            break;
        }
        token_end = strchr(token_start + 1, '\"');
        size_t token_len = token_end - token_start;
        char* key_string = malloc(token_len * sizeof(char));
        key_string[token_len - 1] = '\0';
        strncpy(key_string, token_start + 1, token_end - token_start - 1);

        PyObject* key = NULL;
        if(!(key = Py_BuildValue("s", key_string))) {
            printf("ERROR: Failed to build string value\n");
            return NULL;
        }
        free(key_string);

        // parse value
        token_start = strchr(token_end, ':');
        char* digit = strpbrk(token_start, "-0123456789.eE");
        char* quote = strchr(token_start, '\"');  
        PyObject* value = NULL;
        if(digit == NULL || (quote != NULL && quote < digit)){  // value is string
            token_start = quote;
            token_end = strchr(token_start + 1, '\"');
            size_t token_len = token_end - token_start;
            char* value_string = malloc(token_len * sizeof(char));
            value_string[token_len - 1] = '\0';
            strncpy(value_string, token_start + 1, token_end - token_start - 1);

            if(!(value = Py_BuildValue("s", value_string))) {
                printf("ERROR: Failed to build string value\n");
                return NULL;
            }
            free(value_string);
            token_end++;
        }
        else {  // value is number
            double number = strtod(token_start + 1, (char**)&token_end);
            if(!(value = Py_BuildValue("d", number))) {
                printf("ERROR: Failed to build integer value\n");
                return NULL;
            }
        }

        if(PyDict_SetItem(dict, key, value) < 0) {
            printf("ERROR: Failed to set item\n");
            return NULL;
        }
    }

    return dict;
}

static PyObject* dumps(PyObject* self, PyObject*  args) {
    PyObject *dict = NULL;
    if(!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict)) {
        printf("ERROR: Failed to parse Dict Object\n");
        return NULL;  
    } 
    PyObject* items_list = PyDict_Items(dict);
    size_t list_len = PyList_Size(items_list);

    size_t current_string_size = 3000 + 6 * list_len; // {"k": v}\0;
    char* dict_string = malloc(current_string_size * sizeof(char));
    dict_string[0] = '{';
    dict_string[1] = '\0';

    for(size_t i = 0; i < list_len; ++i) {
        if(i > 0) {
            strcat(dict_string, ", ");
        }

        PyObject* item = PyList_GetItem(items_list, i);
        const char* key_string;
        PyObject* value = NULL;
        if(!PyArg_ParseTuple(item, "sO", &key_string, &value)){
            printf("ERROR: Failed to parse item\n");
        }

        if(strlen(key_string) + 4 + strlen(dict_string) > current_string_size - 1) {
            current_string_size *= 2;
            dict_string = realloc(dict_string, current_string_size * sizeof(char));
        }
        strcat(dict_string,"\"");
        strcat(dict_string, key_string);
        strcat(dict_string, "\": ");

        bool is_number = PyNumber_Check(value);
        if(is_number) {
            if(PyFloat_Check(value)) {
                char str_number[100];
                double number = PyFloat_AsDouble(value);
                sprintf(str_number, "%g", number);
                if(strlen(str_number) + 3 + strlen(dict_string) > current_string_size - 1) {
                    current_string_size *= 2;
                    dict_string = realloc(dict_string, current_string_size * sizeof(char));
                }  
                strcat(dict_string, str_number); 
                continue;
            }
            value = PyNumber_ToBase(value, 10); 
        }

        PyObject* str_repr = PyUnicode_AsEncodedString(value, "utf-8", "~E~");
        const char *value_string = PyBytes_AS_STRING(str_repr);
        if(strlen(value_string) + 5 + strlen(dict_string) > current_string_size - 1) {
            current_string_size *= 2;
            dict_string = realloc(dict_string, current_string_size * sizeof(char));
        }

        if(!is_number){
            strcat(dict_string,"\"");
        }
        strcat(dict_string, value_string);
        if(!is_number){
            strcat(dict_string,"\"");
        }
    }

    strcat(dict_string, "}");
    PyObject* result = Py_BuildValue("s", dict_string); 
    free(dict_string);
    return result;
}


static PyMethodDef methods[] = {
    {"loads", loads, METH_VARARGS, "parse a JSON string and convert it into a Python object"},
    {"dumps", dumps, METH_VARARGS, "dumps a dictionary and returns a JSON string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_cjson = {
    PyModuleDef_HEAD_INIT, "cjson", NULL, -1, methods
};

PyMODINIT_FUNC PyInit_cjson(){
    return PyModule_Create(&module_cjson);
}
