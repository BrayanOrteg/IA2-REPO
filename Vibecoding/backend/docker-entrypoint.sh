#!/bin/bash
# Script de inicialización para el contenedor Docker

echo "🚀 Iniciando QuickTask Backend..."

# Esperar a que la base de datos esté lista
echo "⏳ Esperando inicialización de base de datos..."
sleep 2

# Ejecutar script de datos de prueba si existe
if [ -f "init_dev_data.py" ]; then
    echo "📝 Creando datos de prueba..."
    python init_dev_data.py
fi

echo "✅ Inicialización completada"

# Iniciar el servidor
exec "$@"
