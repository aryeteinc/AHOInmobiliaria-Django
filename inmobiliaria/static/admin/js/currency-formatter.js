/**
 * Formateador de moneda para campos del admin de Django
 * Aplica formato completo de moneda con separadores de miles y millones
 */

(function($) {
    'use strict';

    // Función para formatear número a moneda completa
    function formatCurrency(value) {
        // Limpiar el valor: solo números, puntos y comas
        let cleanValue = value.toString().replace(/[^\d.,]/g, '');
        
        // Remover separadores existentes pero mantener el punto decimal
        cleanValue = cleanValue.replace(/,/g, '');
        
        // Convertir a número
        let number = parseFloat(cleanValue) || 0;
        
        // Formatear con separadores de miles y decimales apropiados
        let formatted = number.toLocaleString('es-CO', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2,
            useGrouping: true
        });
        
        return formatted;
    }

    // Función para obtener valor numérico limpio sin formato
    function getNumericValue(formattedValue) {
        // Remover símbolo de peso, espacios y separadores de miles
        let cleanValue = formattedValue.replace(/[$\s,]/g, '');
        
        // Validar que sea un número válido
        let numericValue = parseFloat(cleanValue);
        
        return isNaN(numericValue) ? '' : cleanValue;
    }

    // Función para validar entrada de números
    function isValidInput(char, currentValue, cursorPosition) {
        // Permitir números, punto decimal, backspace, delete, flechas
        const allowedKeys = ['0','1','2','3','4','5','6','7','8','9','.','Backspace','Delete','ArrowLeft','ArrowRight','Tab'];
        
        if (allowedKeys.includes(char)) {
            // Solo permitir un punto decimal
            if (char === '.' && currentValue.includes('.')) {
                return false;
            }
            return true;
        }
        
        return false;
    }

    // Función para aplicar formateo a un campo
    function setupCurrencyField(field) {
        const $field = $(field);
        
        // Formatear valor inicial si existe
        if ($field.val()) {
            const numericValue = getNumericValue($field.val());
            if (numericValue) {
                $field.val('$' + formatCurrency(numericValue));
            }
        }

        // Validación de teclas presionadas
        $field.on('keydown', function(e) {
            const char = e.key;
            const currentValue = $(this).val();
            
            // Permitir teclas de control (Ctrl+A, Ctrl+C, etc.)
            if (e.ctrlKey || e.metaKey) {
                return true;
            }
            
            // Validar entrada
            if (!isValidInput(char, currentValue, this.selectionStart)) {
                e.preventDefault();
                return false;
            }
        });

        // Evento al escribir en el campo (formateo en tiempo real)
        $field.on('input', function() {
            const cursorPosition = this.selectionStart;
            const oldValue = $(this).val();
            const oldLength = oldValue.length;
            
            // Obtener valor numérico limpio
            const numericValue = getNumericValue(oldValue);
            
            if (numericValue || oldValue === '' || oldValue === '$') {
                let formattedValue = '';
                
                if (numericValue) {
                    formattedValue = '$' + formatCurrency(numericValue);
                } else {
                    formattedValue = '$';
                }
                
                $(this).val(formattedValue);
                
                // Calcular nueva posición del cursor
                const newLength = formattedValue.length;
                const lengthDiff = newLength - oldLength;
                let newPosition = cursorPosition + lengthDiff;
                
                // Asegurar que el cursor no esté antes del símbolo $
                newPosition = Math.max(1, newPosition);
                newPosition = Math.min(newPosition, formattedValue.length);
                
                // Establecer posición del cursor
                this.setSelectionRange(newPosition, newPosition);
            }
        });

        // Evento al perder el foco - limpiar para envío
        $field.on('blur', function() {
            const formattedValue = $(this).val();
            const numericValue = getNumericValue(formattedValue);
            
            // Si hay valor, guardar solo el número; si no, limpiar campo
            $(this).val(numericValue || '');
        });

        // Evento al obtener el foco - mostrar formato
        $field.on('focus', function() {
            const numericValue = $(this).val();
            
            if (numericValue && !isNaN(parseFloat(numericValue))) {
                $(this).val('$' + formatCurrency(numericValue));
            } else if ($(this).val() === '') {
                $(this).val('$');
            }
            
            // Colocar cursor al final
            const length = $(this).val().length;
            this.setSelectionRange(length, length);
        });

        // Prevenir paste de contenido no válido
        $field.on('paste', function(e) {
            e.preventDefault();
            
            const paste = (e.originalEvent.clipboardData || window.clipboardData).getData('text');
            const numericValue = getNumericValue(paste);
            
            if (numericValue) {
                $(this).val('$' + formatCurrency(numericValue));
            }
        });
    }

    // Inicializar cuando el DOM esté listo
    $(document).ready(function() {
        // Aplicar a campos existentes
        $('.currency-input').each(function() {
            setupCurrencyField(this);
        });

        // Para formularios dinámicos (inlines)
        $(document).on('formset:added', function(event, $row) {
            $row.find('.currency-input').each(function() {
                setupCurrencyField(this);
            });
        });
    });

    // Antes de enviar el formulario, asegurar que los valores sean numéricos
    $(document).on('submit', 'form', function() {
        $('.currency-input').each(function() {
            const formattedValue = $(this).val();
            const numericValue = getNumericValue(formattedValue);
            $(this).val(numericValue);
        });
    });

})(django.jQuery);