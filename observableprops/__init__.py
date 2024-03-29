"""
Just a simple utility for automatically creating class properties and adding observers to it.
"""

class ObservableProp:
    def __init__(self, attr, observers_attr):
        self.attr, self.observers_attr = attr, observers_attr

    def get(self, obj):
        return getattr(obj, self.attr)

    def set(self, obj, new):
        if new != getattr(obj, self.attr):
            for f in getattr(obj, self.observers_attr): f(new)
        setattr(obj, self.attr, new)

    def delete(self, obj):
        delattr(obj, self.attr)
        delattr(obj, self.observers_attr)


class ObservablesMeta(type):
    def __new__(mcs, name, bases, attrs):
        class_obj = super().__new__(mcs, name, bases, attrs)
        ObservablesMeta.define_properties(class_obj)
        setattr(class_obj, 'add_observer', ObservablesMeta.add_observer)
        return class_obj

    @staticmethod
    def define_properties(class_obj):
        for nameattr in class_obj.observable_properties:
            holderattr = f"_{nameattr}"
            observers_attr = f"_{nameattr}_observers"
            setattr(class_obj, holderattr, None)
            setattr(class_obj, observers_attr, [])
            prop_obj = property(
                fget=ObservableProp(holderattr, observers_attr).get,
                fset=ObservableProp(holderattr, observers_attr).set,
                fdel=ObservableProp(holderattr, observers_attr).delete,
            )
            setattr(class_obj, nameattr, prop_obj)

        return class_obj

    @staticmethod
    def add_observer(obj, prop_name, observer):
        observers_attr = f"_{prop_name}_observers"
        getattr(obj, observers_attr).append(observer)